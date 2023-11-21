from big_thing_py.big_thing import Event, MXThing, Union
from big_thing_py.manager import Event, MXThing, Union
from big_thing_py.poll_manager_thing import *
from big_thing_py.staff_thing import Event, MXThing, Union
from matter_staff_thing import *
from matter_utils import *
from functools import partialmethod


from matter_server.common.models import APICommand
from matter_server.client.models.device_types import ALL_TYPES as DEVICE_TYPES, DeviceType
from matter_server.client.models import device_types

from chip.clusters import Objects as Cluster
from chip.clusters.ClusterObjects import ALL_ATTRIBUTES, ALL_CLUSTERS

_CLUSTER_T = TypeVar("_CLUSTER_T", bound=Cluster.Cluster)

import asyncio
import subprocess
import shutil


class MXMatterManagerThing(MXPollManagerThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        ip: str = None,
        port: int = None,
        ssl_ca_path: str = None,
        ssl_enable: bool = False,
        log_name: str = None,
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
        manager_mode: MXManagerMode = MXManagerMode.SPLIT,
        scan_cycle=5,
        conf_file_path: str = '',
        conf_select: str = '',
        wifi_credentials: Tuple[str, str] = ('', ''),
        thread_network_dataset: str = '',
        matter_server_clean_start: bool = False,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            ip,
            port,
            ssl_ca_path,
            ssl_enable,
            log_name,
            log_enable,
            log_mode,
            append_mac_address,
            manager_mode,
            scan_cycle,
        )

        self._conf_file_path = conf_file_path
        self._conf_select = conf_select

        self._loop = asyncio.get_event_loop()
        self._matter_server_pid: int = None
        # self._matter_client: MatterClient = None
        self._websocket_client: WebSocketClient = WebSocketClient(
            loop=self._loop, url=f'ws://127.0.0.1:{DEFAULT_WEBSOCKET_PORT}/ws'
        )
        self._matter_server_clean_start: bool = matter_server_clean_start
        self._websocket_message_id: int = 0

        self._vendor_id: int = 0
        self._fabric_id: int = 0
        self._websocket_port: int = 0
        self._pin_code: int = 0
        self._qr_code: str = ''
        self._manual_code: str = ''
        self._is_commissioning: bool = False

        self._wifi_ssid: str = wifi_credentials[0]
        self._wifi_password: str = wifi_credentials[1]
        self._thread_network_dataset: str = thread_network_dataset

        # self._new_matter_device: Queue = Queue()

        if not self._conf_file_path:
            raise Exception('Empty conf file path')
        elif not os.path.exists(self._conf_file_path):
            raise Exception('Invalid conf file path')
        else:
            self._load_config()

    @override
    def setup(self, avahi_enable=True):
        self._kill_matter_server()
        self._matter_server_pid = self._run_matter_server_instance(
            self._vendor_id,
            self._fabric_id,
            self._websocket_port,
            self._matter_server_clean_start,
        )

        super().setup(avahi_enable=avahi_enable)

    @override
    def run(self):
        try:
            self._connect(self._ip, self._port)

            # Start main threads
            for thread in self._comm_thread_list + self._thread_list:
                thread.start()

            if self._manager_mode == MXManagerMode.JOIN:
                self._register()
            elif self._manager_mode == MXManagerMode.SPLIT:
                # SPLIT 모드일 땐, manager thing 자기자신은 등록하지 않는다.
                pass
            else:
                pass

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                self._loop.run_forever()
                time.sleep(1000)
        except KeyboardInterrupt as e:
            MXLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError as e:
            MXLOG_DEBUG('Connection error while connect to broker. Check ip and port', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    @override
    def wrapup(self):
        self._loop.stop()
        self._kill_matter_server(self._matter_server_pid)
        return super().wrapup()

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    @override
    def _alive_publishing_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._manager_mode == MXManagerMode.JOIN:
                    current_time = get_current_time()
                    if current_time - self._last_alive_time > self._alive_cycle:
                        for staff_thing in self._staff_thing_list:
                            self._send_TM_ALIVE(staff_thing)
                elif self._manager_mode == MXManagerMode.SPLIT:
                    # check staff thing is alive
                    current_time = get_current_time()
                    for staff_thing in self._staff_thing_list:
                        if not staff_thing.get_registered():
                            continue

                        if current_time - staff_thing._last_alive_time < staff_thing._alive_cycle:
                            continue

                        if self.interview_matter_thing(staff_thing):
                            staff_thing.set_last_alive_time(current_time)
                            self._send_TM_ALIVE(staff_thing)
                            continue

                        if self.remove_matter_thing(staff_thing):
                            self._send_TM_UNREGISTER(staff_thing)
                            staff_thing._is_connected = False
                            self._staff_thing_list.remove(staff_thing)
                        else:
                            MXLOG_DEBUG(f'Failed to remove staff thing: {staff_thing.get_name()}', 'red')
                else:
                    raise Exception('Invalid Manager Mode')
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    @override
    def _scan_staff_message_thread_func(self, stop_event: Event):
        '''
        scan staff thing periodically and create staff thing instance

        if scanned staff thing is not in self._staff_thing_list, create staff thing instance and
        connect to staff thing
        else if scanned staff thing is in self._staff_thing_list, send alive packet.
        '''

        self.set_wifi_credentials(self._wifi_ssid, self._wifi_password)
        self.set_thread_dataset(self._thread_network_dataset)

        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                # if not (get_current_time() - self._last_scan_time > self._scan_cycle):
                #     continue

                scanned_staff_thing_info_list = self._scan_staff_thing()
                for staff_thing_info in scanned_staff_thing_info_list:
                    # create staff thing instance
                    staff_thing: MXMatterStaffThing = self._create_staff(staff_thing_info)
                    if not staff_thing:
                        continue

                    MXLOG_DEBUG(f'New staff_thing!!! name: [{staff_thing.get_name()}]', 'green')
                    staff_thing._is_connected = True
                    self._send_TM_REGISTER(staff_thing)

                # update the scan cycle to half the minimum alive cycle of all staff thing
                self._scan_cycle = (
                    (min([staff_thing.get_alive_cycle() for staff_thing in self._staff_thing_list]) / 2)
                    if len(self._staff_thing_list) > 0
                    else self._scan_cycle
                )
                # self._last_scan_time = get_current_time()

                commission_code = self.get_commission_code_interactive()
                self.commission_matter_thing(commission_code=commission_code)
                time.sleep(0.5)

                # c = getch()
                # if c == 'c':
                #     commission_code = self.get_commission_code_interactive()
                #     self.commission_matter_thing(commission_code=commission_code)
                #     time.sleep(0.5)
                # elif c == '\x03':
                #     raise KeyboardInterrupt
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    # nothing to add...

    # ===========================
    #            _____   _____
    #     /\    |  __ \ |_   _|
    #    /  \   | |__) |  | |
    #   / /\ \  |  ___/   | |
    #  / ____ \ | |      _| |_
    # /_/    \_\|_|     |_____|
    # ===========================

    def _scan_staff_thing(self, timeout: float = 10) -> List[dict] | bool:
        staff_thing_info_list = []
        commissioned_matter_device_info_list: List[dict] = self.get_matter_thing_list(timeout=timeout)
        # discovered_matter_device_info_list: List[dict] = self.discover_matter_thing(timeout=timeout)

        # for matter_device_info in discovered_matter_device_info_list:
        #     if matter_device_info['pairingHint'] != 33:
        #         continue
        #     device_type: type[DeviceType] = DEVICE_TYPES.get(matter_device_info['deviceType'], None)
        #     staff_thing_info = dict(
        #         name='',
        #         uniqueId='',
        #         vendorId=matter_device_info['vendorId'],
        #         productId=matter_device_info['productId'],
        #         instanceName=matter_device_info['instanceName'],
        #         deviceType=device_type,
        #     )

        #     self._new_matter_device.put(staff_thing_info)
        #     MXLOG_DEBUG(
        #         f'instance_name: {matter_device_info["instanceName"]}, device_type: {device_type.__name__} discovered.'
        #     )

        for matter_device_info in commissioned_matter_device_info_list:
            # cluster_type_list: List[type[_CLUSTER_T]] = list(device_type.clusters)
            # cluster_list: Objects.Cluster = [
            #     ALL_CLUSTERS[ChipClusters.ListClusterInfo(None)[cluster_type.__name__]['clusterId']]
            #     for cluster_type in cluster_type_list
            # ]

            attributes: dict = matter_device_info['attributes']
            vendor_id = attributes[
                f'0/{BasicInformation.Attributes.VendorID.cluster_id}/{BasicInformation.Attributes.VendorID.attribute_id}'
            ]
            product_id = attributes[
                f'0/{BasicInformation.Attributes.ProductID.cluster_id}/{BasicInformation.Attributes.ProductID.attribute_id}'
            ]
            device_type = DEVICE_TYPES.get(
                attributes[
                    f'1/{Descriptor.Attributes.DeviceTypeList.cluster_id}/{Descriptor.Attributes.DeviceTypeList.attribute_id}'
                ][0]['deviceType'],
                None,
            )
            unique_id = attributes.get(
                f'0/{BasicInformation.Attributes.UniqueID.cluster_id}/{BasicInformation.Attributes.UniqueID.attribute_id}',
                str(matter_device_info['node_id']),
            )
            staff_thing_info = dict(
                name=f'{device_type.__name__}_{unique_id}',
                nodeId=matter_device_info['node_id'],
                uniqueId=unique_id,
                vendorId=vendor_id,
                productId=product_id,
                instanceName='',
                deviceType=device_type,
            )

            staff_thing = self._get_staff_thing_by_staff_thing_id(unique_id)
            if not staff_thing:
                staff_thing_info_list.append(staff_thing_info)

        return staff_thing_info_list

    def _create_staff(self, staff_thing_info: dict) -> MXMatterStaffThing | None:
        node_id: int = staff_thing_info['nodeId']
        vendorId: str = staff_thing_info['vendorId']
        productId: str = staff_thing_info['productId']
        uniqueId: str = staff_thing_info['uniqueId']
        instanceName: str = staff_thing_info['instanceName']
        deviceType: type[DeviceType] = staff_thing_info['deviceType']

        staff_thing_id = instanceName if instanceName else uniqueId
        if deviceType == device_types.OnOffLight:
            matter_staff_thing = MXOnOffLightMatterStaffThing(
                name=f'{deviceType.__name__}_{staff_thing_id}',
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                node_id=node_id,
                vendor_id=vendorId,
                product_id=productId,
                device_type=deviceType,
                send_api_command_func=self.send_api_command,
            )
        elif deviceType == device_types.DimmableLight:
            matter_staff_thing = MXDimmableLightMatterStaffThing(
                name=f'{deviceType.__name__}_{staff_thing_id}',
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                node_id=node_id,
                vendor_id=vendorId,
                product_id=productId,
                device_type=deviceType,
                send_api_command_func=self.send_api_command,
            )
        elif deviceType == device_types.ContactSensor:
            matter_staff_thing = MXContactSensorMatterStaffThing(
                name=f'{deviceType.__name__}_{staff_thing_id}',
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                node_id=node_id,
                vendor_id=vendorId,
                product_id=productId,
                device_type=deviceType,
                send_api_command_func=self.send_api_command,
            )
        elif deviceType == device_types.OnOffPlugInUnit:
            matter_staff_thing = MXOnOffPlugInUnitMatterStaffThing(
                name=f'{deviceType.__name__}_{staff_thing_id}',
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                node_id=node_id,
                vendor_id=vendorId,
                product_id=productId,
                device_type=deviceType,
                send_api_command_func=self.send_api_command,
            )
        else:
            MXLOG_DEBUG(
                f'Not supported product!!! name: {staff_thing_info["name"]}, type: {staff_thing_info["type"]}',
                'yellow',
            )
            return None

        matter_staff_thing.make_service_list()
        matter_staff_thing.set_function_result_queue(self._publish_queue)

        for service in matter_staff_thing.get_value_list() + matter_staff_thing.get_function_list():
            service.remove_tag(matter_staff_thing.get_name())

        return matter_staff_thing

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _load_config(self):
        conf_file: dict = json_file_read(self._conf_file_path)

        if not conf_file:
            return

        self._vendor_id = convert_to_int(conf_file.get('vendor_id', None))
        self._fabric_id = convert_to_int(conf_file.get('fabric_id', None))
        self._websocket_port = convert_to_int(conf_file.get('websocket_port', None))
        self._pin_code = convert_to_int(conf_file.get('pin_code', None))
        self._qr_code = conf_file.get('QR_code', None)
        self._manual_code = conf_file.get('manual_code', None)

    def _run_matter_server_instance(
        self,
        vendor_id: int = DEFAULT_VENDOR_ID,
        fabric_id: int = DEFAULT_FABRIC_ID,
        websocket_port: int = DEFAULT_WEBSOCKET_PORT,
        clean_start: bool = False,
    ) -> Tuple[int]:
        if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 10):
            raise Exception("Python 3.10 or higher is required.")

        matter_server_instance_name = 'matter_server_instance.py'
        storage_path = os.path.join(Path.home(), ".matter_server")
        if clean_start:
            self._kill_matter_server()
            shutil.rmtree(storage_path)
        os.makedirs(storage_path, exist_ok=True)

        process = subprocess.Popen(
            f'python3 {matter_server_instance_name} --port {websocket_port} --vendor-id {vendor_id} --fabric-id {fabric_id}',
            shell=True,
        )
        pid = process.pid

        while True:
            try:
                time.sleep(0.5)
                if self._websocket_client.connect():
                    break
            except Exception as e:
                continue

        return pid

    def _kill_matter_server(self, pid: int = None):
        if pid:
            subprocess.Popen(f'kill -9 {pid}', shell=True)
        else:
            try:
                output = subprocess.check_output(
                    'ps aux | grep matter_server_instance.py | grep -v grep | awk \'{print $2}\'', shell=True, text=True
                )
                pid = [o.strip() for o in output.split()]
                for p in pid:
                    subprocess.Popen(f'kill -9 {p}', shell=True)

            except subprocess.CalledProcessError:
                print("matter_server_instance.py is not running")

    def get_commission_code_interactive(self) -> str:
        commission_code = (
            input(
                f'Enter {colored("pin code", "green")} or {colored("QR code", "cyan")} or {colored("manual code", "cyan")}: '
            )
            or ''
        )
        return commission_code

    def send_api_command(self, command: dict, timeout: float = 10) -> Union[dict, bool]:
        while self._is_commissioning:
            time.sleep(THREAD_TIME_OUT)

        if 'commission' in command['command']:
            self._is_commissioning = True
        command_result = self._websocket_client.sync_send_request(command, timeout)
        if 'commission' in command['command']:
            self._is_commissioning = False

        try:
            command_result_dict = json.loads(command_result)
            return command_result_dict
        except Exception:
            return False

    #################################################################################################################################

    def set_wifi_credentials(self, ssid: str, password: str, timeout: float = 10) -> bool:
        try:
            result = self.send_api_command(
                command={
                    'message_id': f'set_wifi_credentials_{self._websocket_message_id}',
                    'command': APICommand.SET_WIFI_CREDENTIALS.value,
                    'args': {
                        'ssid': ssid,
                        'credentials': password,
                    },
                },
                timeout=timeout,
            )
            self._websocket_message_id += 1

            return result.get('result', False)
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def set_thread_dataset(self, dataset: str, timeout: float = 10) -> bool:
        try:
            result = self.send_api_command(
                command={
                    'message_id': f'set_thread_dataset_{self._websocket_message_id}',
                    'command': APICommand.SET_THREAD_DATASET.value,
                    'args': {
                        'dataset': dataset,
                    },
                },
                timeout=timeout,
            )
            self._websocket_message_id += 1

            return result.get('result', False)
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def discover_matter_thing(self, timeout: float = 10) -> Union[List[dict], bool]:
        try:
            result = self.send_api_command(
                command={
                    'message_id': f'discover_{self._websocket_message_id}',
                    'command': APICommand.DISCOVER.value,
                },
                timeout=timeout,
            )
            self._websocket_message_id += 1

            return result.get('result', False)
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def commission_matter_thing(
        self, commission_code: Union[int, str], timeout: float = 10
    ) -> Union[Tuple[int, str, str], bool]:
        pin_code, qr_code, manual_code = None, None, None

        if commission_code == None:
            pin_code = self._pin_code
            qr_code = self._qr_code
            manual_code = self._manual_code
        elif len(commission_code) == 8:
            pin_code = int(commission_code)
        elif len(commission_code) == 11:
            manual_code = commission_code
            timeout = 30
        elif commission_code.startswith('MT'):
            qr_code = commission_code
            timeout = 30
        else:
            MXLOG_DEBUG(f'Invalid commission code: {commission_code}', 'red')
            return False

        try:
            if not (qr_code or manual_code):
                command = APICommand.COMMISSION_ON_NETWORK.value
                args = {'setup_pin_code': pin_code}
            else:
                command = APICommand.COMMISSION_WITH_CODE.value
                if qr_code:
                    args = {'code': qr_code}
                elif manual_code:
                    args = {'code': manual_code}

            result = self.send_api_command(
                command={
                    'message_id': f'{command}_{self._websocket_message_id}',
                    'command': command,
                    'args': args,
                },
                timeout=timeout,
            )
            self._websocket_message_id += 1

            if not result:
                return False
            elif 'error_code' in result:
                error_code = result['error_code']
                details = result['details']
                MXLOG_DEBUG(f'error_code: {error_code}, details: {details}', 'red')
                return False
            else:
                node_id = result['result']['node_id']
                device_type = DEVICE_TYPES.get(
                    result['result']['attributes'][
                        f'1/{Descriptor.Attributes.DeviceTypeList.cluster_id}/{Descriptor.Attributes.DeviceTypeList.attribute_id}'
                    ][0]['deviceType'],
                    None,
                )
                unique_id = result['result']['attributes'][
                    f'0/{BasicInformation.Attributes.UniqueID.cluster_id}/{BasicInformation.Attributes.UniqueID.attribute_id}'
                ]
                name = f'{device_type.__name__}_{unique_id}'
                return node_id, name, unique_id
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def get_matter_thing_list(self, timeout: float = 10) -> Union[List[dict], bool]:
        try:
            result = self.send_api_command(
                command={
                    'message_id': '1',
                    'command': APICommand.GET_NODES.value,
                },
                timeout=timeout,
            )

            return result.get('result', False)
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def get_matter_thing(self, node_id: int, timeout: float = 10) -> Union[dict, bool]:
        try:
            result = self.send_api_command(
                command={
                    'message_id': '1',
                    'command': APICommand.GET_NODE.value,
                    'args': {
                        'node_id': node_id,
                    },
                },
                timeout=timeout,
            )

            return result.get('result', False)
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def interview_matter_thing(self, matter_staff_thing: MXMatterStaffThing, timeout: float = 10) -> bool:
        try:
            result = self.send_api_command(
                command={
                    'message_id': '1',
                    'command': APICommand.INTERVIEW_NODE.value,
                    'args': {
                        'node_id': matter_staff_thing._node_id,
                    },
                },
                timeout=timeout,
            )

            if result.get('result', False) == None:
                return True
            else:
                error_code = result['result']['error_code']
                details = result['result']['details']
                MXLOG_DEBUG(f'error_code: {error_code}, details: {details}', 'red')
                return False
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False

    def remove_matter_thing(self, matter_staff_thing: MXMatterStaffThing, timeout: float = 10) -> bool:
        try:
            result = self.send_api_command(
                command={
                    'message_id': '1',
                    'command': APICommand.REMOVE_NODE.value,
                    'args': {
                        'node_id': matter_staff_thing._node_id,
                    },
                },
                timeout=timeout,
            )

            if result.get('result', False) == None:
                return True
            else:
                error_code = result['result']['error_code']
                details = result['result']['details']
                MXLOG_DEBUG(f'error_code: {error_code}, details: {details}', 'red')
                return False
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'send_api_command failed. result: {result}', 'red')
            return False
