from big_thing_py.poll_manager_thing import *

from hejhome_staff_thing import *
from hejhome_utils import *
import pika
from func_timeout import func_timeout


class MXHejhomeManagerThing(MXPollManagerThing):
    API_HEADER_TEMPLATE = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json;charset-UTF-8"
        # "Host": self.endpoint_host,
        # "Referer": "https://{host}".format(host=self.host),
        # "Accept": "*/*",
        # "Connection": "close",
    }

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
        conf_file_path: str = 'config.json',
        conf_select: str = '',
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

        self._staff_thing_list: List[MXHejhomeStaffThing] = []
        self._conf_file_path = conf_file_path
        self._conf_select = conf_select

        self._endpoint_host = ''
        self._api_token = ''
        self._client_id = ''
        self._client_secret = ''
        self._header = {}

        if not self._conf_file_path:
            raise Exception('Empty conf file path')
        elif not os.path.exists(self._conf_file_path):
            raise Exception('Invalid conf file path')
        else:
            self._load_config()

        self._endpoint_scan_homes = f'{self._endpoint_host}/homes'
        self._endpoint_get_whole_device = f'{self._endpoint_host}/devices'
        self._endpoint_scan_rooms = f'{self._endpoint_host}/homes/%s/rooms'  # %s: home_id
        self._endpoint_scan_devices = f'{self._endpoint_host}/homes/%s/rooms/%s/devices'  # %s: home_id, room_id
        self._endpoint_device_control = f'{self._endpoint_host}/control/%s'  # %s: device_id
        self._endpoint_get_device_state = f'{self._endpoint_host}/device/%s'  # %s: device_id

        # Threading
        self._thread_func_list += [self.AMQP_listening_thread_func]

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def AMQP_listening_thread_func(self, stop_event: Event):
        def callback(ch, method, properties, body):
            json_body = json.loads(body)
            # print(f" [AMQP] Received {json_body}")

            try:
                devId = json_body['deviceDataReport']['devId']
                # dataId = json_body['deviceDataReport']['dataId']
                status = json_body['deviceDataReport']['status']
                pir_status = status[0]
            except Exception as e:
                print_error(e)
                pir_status = dict(value=None)
                return False

            for staff_thing in self._staff_thing_list:
                if staff_thing._staff_thing_id == devId:
                    if isinstance(staff_thing, MXRadarPIRSensorHejhomeStaffThing):
                        if pir_status['value'] == 'pir':
                            staff_thing._pir_status = pir_status
                            break

        try:
            res = API_request(
                f'{self._endpoint_host}/subscription?clientId={self._client_id}',
                RequestMethod.POST,
                header=self._header,
            )
            if not res:
                raise Exception('Failed to subscribe')

            credentials = pika.PlainCredentials(self._client_id, self._client_secret)
            cxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_options = pika.SSLOptions(context=cxt, server_hostname="goqual.io")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='goqual.io', port=55001, credentials=credentials, ssl_options=ssl_options
                )
            )
            channel = connection.channel()
            # channel.queue_declare(queue=self._client_id)

            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                channel.basic_consume(queue=self._client_id, on_message_callback=callback, auto_ack=True)
                try:
                    func_timeout(1, channel.start_consuming, args=())
                except FunctionTimedOut:
                    channel.stop_consuming()
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

    def _scan_staff_thing(self, timeout: float = 10) -> Union[List[dict], bool]:
        staff_thing_info_list = []

        whole_device_list = API_request(
            self._endpoint_get_whole_device, RequestMethod.GET, self._header, timeout=timeout
        )
        if not whole_device_list:
            MXLOG_DEBUG('Failed to scan devices', 'red')
            return []
        for device in whole_device_list:
            staff_thing_info_list.append(dict(staff_thing_info=device))

        # home_list = API_request(self._endpoint_scan_homes, RequestMethod.GET, self._header, timeout=timeout)
        # if home_list is False:
        #     MXLOG_DEBUG('Failed to scan homes', 'red')
        #     return False
        # for home in home_list['result']:
        #     home_name = home['name']
        #     home_id = home['homeId']
        #     room_list = API_request(
        #         self._endpoint_scan_rooms % (home_id), RequestMethod.GET, self._header, timeout=timeout
        #     )
        #     if room_list is False:
        #         MXLOG_DEBUG('Failed to scan rooms', 'red')
        #         return False
        #     for room in room_list['rooms']:
        #         room_name = room['name']
        #         room_id = room['room_id']
        #         device_list = API_request(
        #             self._endpoint_scan_devices % (home_id, room_id), RequestMethod.GET, self._header, timeout=timeout
        #         )
        #         if device_list is False:
        #             MXLOG_DEBUG('Failed to scan devices', 'red')
        #             return False
        #         for device in device_list:
        #             staff_thing_info_list.append(
        #                 dict(
        #                     home_name=home_name,
        #                     home_id=home_id,
        #                     room_name=room_name,
        #                     room_id=room_id,
        #                     staff_thing_info=device,
        #                 )
        #             )

        return staff_thing_info_list

    def _create_staff(self, staff_thing_info: dict) -> MXHejhomeStaffThing:
        trans = str.maketrans({' ': '_', '(': '_', ')': '_', '-': '_'})

        home_name = staff_thing_info.get('home_name', '')
        home_id = staff_thing_info.get('home_id', '')
        room_name = staff_thing_info.get('room_name', '')
        room_id = staff_thing_info.get('room_id', '')
        staff_thing_info = staff_thing_info['staff_thing_info']

        name = staff_thing_info['name'].translate(trans)
        staff_thing_id = staff_thing_info['id']
        device_type = staff_thing_info['deviceType']
        # has_sub_devices = staff_thing_info['hasSubDevices']
        # model_name = staff_thing_info['modelName']
        # category = staff_thing_info['category']
        # online = staff_thing_info['online']

        if device_type == 'BruntPlug':
            hejhome_staff_thing = MXBruntPlugHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'Curtain':
            hejhome_staff_thing = MXCurtainHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'ZigbeeSwitch3':
            hejhome_staff_thing = MXZigbeeSwitch3HejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'IrDiy':
            hejhome_staff_thing = MXIrDiyHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'IrAirconditioner':
            hejhome_staff_thing = MXIrAirconditionerHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'LedStripRgbw2':
            hejhome_staff_thing = MXLedStripRgbw2HejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'IrTv':
            hejhome_staff_thing = MXIrTvHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif device_type == 'SensorRadar':
            hejhome_staff_thing = MXRadarPIRSensorHejhomeStaffThing(
                name=name,
                service_list=[],
                alive_cycle=60,
                staff_thing_id=staff_thing_id,
                home_name=home_name,
                home_id=home_id,
                room_name=room_name,
                room_id=room_id,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
                pir_status_timeout=5,
            )
        else:
            MXLOG_DEBUG(f'Unexpected device type!!! - {device_type}', 'red')
            raise Exception('Unexpected device type!!!')

        hejhome_staff_thing.make_service_list()
        hejhome_staff_thing.set_function_result_queue(self._publish_queue)
        for staff_service in hejhome_staff_thing.get_value_list() + hejhome_staff_thing.get_function_list():
            staff_service.add_tag(MXTag(self._conf_select))

        return hejhome_staff_thing

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

        if conf_file:
            config_list = conf_file['account_list']
            if not self._conf_select or self._conf_select not in [config['name'] for config in config_list]:
                if len(config_list) == 1:
                    if self._conf_select:
                        cprint(f'Selected config [{self._conf_select}] was not in conf file!!!', 'red')
                    else:
                        cprint(f'Config was not selected!!!', 'red')
                    config = config_list[0]
                    self._conf_select = config['name']
                    cprint(
                        f'Auto Load [{self._conf_select}] config setting [{self._conf_file_path}] from config file',
                        'green',
                    )
                    cprint(f'{config["name"]} : api token={config["api_token"]}', 'yellow')

                    # FIXME: Uncomment this line
                    # cprint(f'Start to run... sleep 3 sec', 'yellow')
                    # time.sleep(3)
                else:
                    user_input = cprint(f'- Please select config -', 'green')
                    for i, config in enumerate(config_list):
                        cprint(f'{i+1:>2}| [{config["name"]}] : api token={config["api_token"]}', 'yellow')
                    user_input = input(f'Please select config : ')
                    if user_input.isdigit():
                        user_input = int(user_input) - 1
                        self._conf_select = config_list[user_input]['name']
                    else:
                        self._conf_select = user_input
                    cprint(
                        f'Load [{self._conf_select}] config setting [{self._conf_file_path}] from config file', 'green'
                    )

            self._endpoint_host, self._api_token, self._client_id, self._client_secret = self._extract_info_from_config(
                conf_file, self._conf_select
            )
            self._header = self._make_header(self._api_token)
        elif self._endpoint_host == '' or self._endpoint_host == None:
            raise Exception('endpoint host is empty. exit program...')
        else:
            raise Exception('config file is empty. exit program...')

        self._endpoint_host = self._endpoint_host.rstrip('/')

    def _extract_info_from_config(self, conf_file: dict, conf_select: str) -> Union[Tuple[str, str], bool]:
        account_list = conf_file['account_list']

        for account in account_list:
            account_name = account['name']
            if account_name == conf_select:
                endpoint_host = account['endpoint_host']
                api_token = account['api_token']
                client_id = account['client_id']
                client_secret = account['client_secret']
                return endpoint_host, api_token, client_id, client_secret

        return False

    def _make_header(self, api_token: str):
        header = MXHejhomeManagerThing.API_HEADER_TEMPLATE
        header['Authorization'] = header['Authorization'] + api_token
        return header

    ##############################################################################################################################

    def _device_value_service_func(self, staff_thing_id: str, action: HejHomeAction) -> dict:
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == HejHomeAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET, url=endpoint_get_device_state % staff_thing_id, header=header
            )
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False

    def _device_function_service_func(
        self,
        staff_thing_id: str,
        action: HejHomeAction,
        brightness: int = None,
        color: Tuple[int, int, int] = None,
        zb_sw: Tuple[bool, bool, bool] = None,
        curtain_percent: int = None,
    ) -> dict:
        endpoint_device_control = self._endpoint_device_control
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == HejHomeAction.ON:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"power": True}}),
                header=header,
            )
        elif action == HejHomeAction.OFF:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"power": False}}),
                header=header,
            )
        elif action == HejHomeAction.ZBSW_ON:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string(
                    {
                        "requirments": {
                            "power1": True,
                            "power2": True,
                            "power3": True,
                        }
                    }
                ),
                header=header,
            )
        elif action == HejHomeAction.ZBSW_OFF:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string(
                    {
                        "requirments": {
                            "power1": False,
                            "power2": False,
                            "power3": False,
                        }
                    }
                ),
                header=header,
            )
        elif action == HejHomeAction.ZBSW_CONTROL:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string(
                    {
                        "requirments": {
                            "power1": zb_sw[0],
                            "power2": zb_sw[1],
                            "power3": zb_sw[2],
                        }
                    }
                ),
                header=header,
            )
        elif action == HejHomeAction.CURTAIN_OPEN:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"control": "open", "percentControl": 100}}),
                header=header,
            )
        elif action == HejHomeAction.CURTAIN_CLOSE:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"control": "open", "percentControl": 0}}),
                header=header,
            )
        elif action == HejHomeAction.CURTAIN_CONTROL:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"control": "open", "percentControl": curtain_percent}}),
                header=header,
            )
        elif action == HejHomeAction.BRIGHTNESS:
            if not isinstance(brightness, int):
                raise Exception('brightness must be int type')
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string({"requirments": {"brightness": brightness}}),
                header=self._header,
            )
        elif action == HejHomeAction.COLOR:
            if not isinstance(color, tuple):
                raise Exception('color must be tuple type')

            hue, saturation, brightness = rgb_to_hsv(*color)
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                # TODO: 색깔 조절이 생각하는대로 되지 않음. rgb 변환을 어떻게 하는지 확인이 필요
                body=dict_to_json_string(
                    {"requirments": {"hsvColor": {"hue": hue, "saturation": saturation, "brightness": brightness}}}
                ),
                header=self._header,
            )
        elif action == HejHomeAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET, url=endpoint_get_device_state % staff_thing_id, header=self._header
            )
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False
