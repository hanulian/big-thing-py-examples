from big_thing_py.manager_thing import *
from smartthings_staff_thing import *
from smartthings_utils import *


class SoPSmartThingsManagerThing(SoPManagerThing):

    API_HEADER_TEMPLATE = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json;charset-UTF-8"
        # "Host": self.endpoint_host,
        # "Referer": "https://{host}".format(host=self.host),
        # "Accept": "*/*",
        # "Connection": "close",
    }

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 manager_mode: SoPManagerMode = SoPManagerMode.SPLIT, scan_cycle=5,
                 endpoint_host: str = '', api_token: str = '', conf_file_path: str = 'smartthings_conf.json', conf_select: str = '',):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port, ssl_ca_path,
                         ssl_enable, log_name, log_enable, log_mode, append_mac_address, manager_mode, scan_cycle)

        self._staff_thing_list: List[SoPSmartThingsStaffThing] = []
        self._conf_file_path = conf_file_path
        self._conf_select = conf_select

        if self._conf_file_path and '' not in [endpoint_host, api_token]:
            self._endpoint_host = endpoint_host.rstrip('/')
            self._api_token = api_token
            self._header = self._make_header(self._api_token)
        else:
            self._load_config()

        self._endpoint_scan_location = f'{self._endpoint_host}/locations'
        self._endpoint_scan_room = f'{self._endpoint_host}/locations/%s/rooms'
        self._endpoint_scan_device = f'{self._endpoint_host}/devices'
        self._endpoint_get_device_detail_info = f'{self._endpoint_host}/devices/%s'
        self._endpoint_get_device_state = f'{self._endpoint_host}/devices/%s/status'
        self._endpoint_device_control = f'{self._endpoint_host}/devices/%s/commands'

    def setup(self, avahi_enable=True):
        return super().setup(avahi_enable=avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    # override
    def _alive_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._manager_mode == SoPManagerMode.JOIN:
                    current_time = get_current_time()
                    if current_time - self._last_alive_time > self._alive_cycle:
                        for staff_thing in self._staff_thing_list:
                            self._send_TM_ALIVE(
                                thing_name=staff_thing.get_name())
                            staff_thing._last_alive_time = current_time
                elif self._manager_mode == SoPManagerMode.SPLIT:
                    # api 방식일 때에는 staff thing이 계속 staff_thing_list에 남아있는 것으로 alive를 처리한다.
                    current_time = get_current_time()
                    for staff_thing in self._staff_thing_list:
                        if current_time - staff_thing._last_alive_time > staff_thing._alive_cycle:
                            self._send_TM_ALIVE(thing_name=staff_thing._name)
                            staff_thing._last_alive_time = current_time
                    pass
                else:
                    raise Exception('Invalid Manager Mode')
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

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    # override
    def _scan_staff_thing(self, timeout: float = 5) -> List[dict]:
        staff_thing_info_list = []

        whole_location_info = dict(location_list=[])
        res = API_request(url=self._endpoint_scan_location,
                          method=RequestMethod.GET, header=self._header)
        if not res:
            raise Exception('Failed to get location info')
        location_list = res['items']
        for location in location_list:
            location_info = dict(name=location['name'],
                                 id=location['locationId'],
                                 room_list=[])
            res = API_request(url=self._endpoint_scan_room % location['locationId'],
                              method=RequestMethod.GET, header=self._header)
            if not res:
                raise Exception('Failed to get room info')
            room_list = res['items']
            for room in room_list:
                room_info = dict(name=room['name'],
                                 id=room['roomId'],
                                 device_list=[])
                location_info['room_list'].append(room_info)
            whole_location_info['location_list'].append(location_info)

        res = API_request(url=self._endpoint_scan_device,
                          method=RequestMethod.GET, header=self._header)
        if not res:
            raise Exception('Failed to get device info')
        device_list = res['items']
        # device type candidate: ['OCF', 'VIPER', 'MOBILE']
        device_list = [
            device for device in device_list if device['type'] != 'MOBILE']

        for device in device_list:
            for location in whole_location_info['location_list']:
                location_name = location['name']
                location_id = location['id']
                for room in location['room_list']:
                    room_name = room['name']
                    room_id = room['id']
                    if device['roomId'] == room_id and device['locationId']:
                        device['location_name'] = location_name
                        device['room_name'] = room_name
                        room['device_list'].append(device)

        staff_thing_info_list = device_list
        return staff_thing_info_list

    # override
    def _receive_staff_message(self):
        for staff_thing in self._staff_thing_list:
            try:
                staff_msg = staff_thing._receive_queue.get(
                    timeout=THREAD_TIME_OUT)
                return staff_msg
            except Empty:
                pass

    # override
    def _publish_staff_message(self, msg):
        pass

    # override
    def _parse_staff_message(self, staff_msg) -> Tuple[SoPProtocolType, str, str]:
        protocol = staff_msg['protocol']
        device_id = staff_msg['device_id']
        payload = staff_msg['payload']

        return protocol, device_id, payload

    def _create_staff(self, staff_thing_info: dict) -> SoPSmartThingsStaffThing:
        location_name = staff_thing_info['location_name']
        location_id = staff_thing_info['locationId']
        room_name = staff_thing_info['room_name']
        room_id = staff_thing_info['roomId']
        name = staff_thing_info['name']
        device_id = staff_thing_info['deviceId']
        label = staff_thing_info['label']
        type = staff_thing_info['type']
        device_type_name = staff_thing_info.get('deviceTypeName', None)

        if device_type_name == 'Samsung OCF TV':
            smartthings_staff_thing = SoPTVSmartThingsStaffThing(
                name=name, service_list=[], alive_cycle=60, device_id=device_id,
                label=label, location_name=location_name, location_id=location_id, room_name=room_name, room_id=room_id,
                device_function_service_func=self._device_function_service_func, device_value_service_func=self._device_value_service_func)
        elif device_type_name == 'Samsung OCF Air Purifier':
            smartthings_staff_thing = SoPAirPurifierSmartThingsStaffThing(
                name=name, service_list=[], alive_cycle=60, device_id=device_id,
                label=label, location_name=location_name, location_id=location_id, room_name=room_name, room_id=room_id,
                device_function_service_func=self._device_function_service_func, device_value_service_func=self._device_value_service_func)
        elif device_type_name == 'Samsung OCF Robot Vacuum':
            smartthings_staff_thing = SoPRobotVacuumSmartThingsStaffThing(
                name=name, service_list=[], alive_cycle=60, device_id=device_id,
                label=label, location_name=location_name, location_id=location_id, room_name=room_name, room_id=room_id,
                device_function_service_func=self._device_function_service_func, device_value_service_func=self._device_value_service_func)
        else:
            if type == 'VIPER':
                smartthings_staff_thing = SoPNonSmartThingsStaffThing(
                    name=name, service_list=[], alive_cycle=60, device_id=device_id,
                    label=label, location_name=location_name, location_id=location_id, room_name=room_name, room_id=room_id,
                    device_function_service_func=self._device_function_service_func, device_value_service_func=self._device_value_service_func)
            else:
                SOPLOG_DEBUG(
                    f'Unexpected device type!!! - {device_type_name}', 'red')
                raise Exception('Unexpected device type!!!')

        smartthings_staff_thing.make_service_list()
        smartthings_staff_thing.set_function_result_queue(self._publish_queue)
        for staff_service in smartthings_staff_thing.get_value_list() + smartthings_staff_thing.get_function_list():
            staff_service.add_tag(SoPTag(self._conf_select))

        return smartthings_staff_thing

    # override

    def _connect_staff_thing(self, staff_thing: SoPStaffThing) -> bool:
        # api 방식에서는 api 요청 결과에 staff thing이 포함되어 있으면 연결.
        staff_thing._receive_queue.put(dict(device_id=staff_thing.get_device_id(),
                                            protocol=SoPProtocolType.Base.TM_REGISTER,
                                            payload=staff_thing.dump()))
        staff_thing._is_connected = True

    # override
    def _disconnect_staff_thing(self, staff_thing: SoPStaffThing) -> bool:
        # api 방식에서는 api 요청 결과에 staff thing이 포함되어 있지 않으면 연결해제.
        staff_thing._is_connected = False

    # override
    def _handle_REGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> Tuple[str, dict]:
        return staff_thing.get_name(), payload

    # override
    def _handle_UNREGISTER_staff_message(self, staff_thing: SoPStaffThing) -> str:
        self._send_TM_UNREGISTER(staff_thing.get_name())

    # override
    def _handle_ALIVE_staff_message(self, staff_thing: SoPStaffThing) -> str:
        pass

    # override
    def _handle_VALUE_PUBLISH_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> Tuple[str, str, dict]:
        pass

    # override
    def _handle_RESULT_EXECUTE_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> str:
        # API 방식의 staff thing으로 부터는 result 메시지를 받지 않는다.
        pass

    # override
    def _send_RESULT_REGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        # API 방식의 staff thing에게는 result 메시지를 보내지 않는다.
        pass

    # override
    def _send_RESULT_UNREGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        # API 방식의 staff thing에게는 result 메시지를 보내지 않는다.
        pass

    # override
    def _send_EXECUTE_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        # API 방식의 staff thing에게는 execute 메시지를 보내지 않는다. 대시 execute 동작을 하는 api 요청을 보낸다.
        pass

    ##############################################################################################################################

    def _load_config(self):
        conf_file = json_file_read(self._conf_file_path)

        if conf_file:
            SOPLOG_DEBUG(
                f'Load [{self._conf_select}] config setting from config file [{self._conf_file_path}]', 'yellow')

            self._endpoint_host, self._api_token = self._extract_info_from_config(
                conf_file, self._conf_select)
            self._header = self._make_header(self._api_token)
        elif self._endpoint_host == '' or self._endpoint_host == None:
            SOPLOG_DEBUG('endpoint host is empty. exit program...', 'red')
            raise

        self._endpoint_host = self._endpoint_host.rstrip('/')

    def _extract_info_from_config(self, conf_file: dict, conf_select: str) -> Union[Tuple[str, str], bool]:
        account_list = conf_file['account_list']

        for account in account_list:
            account_name = account['name']
            if account_name == conf_select:
                endpoint_host = account['endpoint_host']
                api_token = account['api_token']
                return endpoint_host, api_token

        return False

    def _make_header(self, api_token: str):
        header = SoPSmartThingsManagerThing.API_HEADER_TEMPLATE
        header['Authorization'] = header['Authorization'] + api_token
        return header

    ##############################################################################################################################

    def _device_value_service_func(self, device_id: str, action: SmartThingsAction) -> dict:
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == SmartThingsAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET,
                url=endpoint_get_device_state % device_id,
                header=header)
        else:
            raise Exception('invalid action')

        if ret:
            return True
        else:
            return False

    # TODO: smartthings는 각 디바이스에 대한 커맨드목록을 제공한다. 이를 통해 미리 action을 정의 하지않고도 커맨드를 날릴 수 있다.
    # TODO: 현재는 action을 미리 정의해서 사용하는 방식으로 구현하였다. 나중에 위의 방법으로 바꾸어야함.
    def _device_function_service_func(self, device_id: str, action: SmartThingsAction) -> dict:
        endpoint_device_control = self._endpoint_device_control
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == SmartThingsAction.ON:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % device_id,
                body=dict_to_json_string({
                    "commands": [
                        {
                            "component": "main",
                            "capability": "switch",
                            "command": "on"
                        }
                    ]
                }),
                header=header)
        elif action == SmartThingsAction.OFF:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % device_id,
                body=dict_to_json_string({
                    "commands": [
                        {
                            "component": "main",
                            "capability": "switch",
                            "command": "off"
                        }
                    ]
                }),
                header=header)
        elif action == SmartThingsAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET,
                url=endpoint_get_device_state % device_id,
                header=self._header)
        else:
            raise Exception('invalid action')

        if ret:
            return True
        else:
            return False
