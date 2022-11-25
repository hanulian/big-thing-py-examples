from big_thing_py.manager_thing import *
from hue_staff_thing import *
from hue_utils import *


class SoPHueManagerThing(SoPManagerThing):

    API_HEADER_TEMPLATE = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json;charset-UTF-8"
        # "Host": self.endpoint_host,
        # "Referer": "https://{host}".format(host=self.host),
        # "Accept": "*/*",
        # "Connection": "close",
    }

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True, manager_mode: SoPManagerMode = SoPManagerMode.SPLIT, scan_cycle=5,
                 endpoint_host: str = '', api_token='', conf_file_path: str = '', conf_select: str = ''):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port, ssl_ca_path,
                         ssl_enable, log_name, log_enable, log_mode, append_mac_address, manager_mode, scan_cycle)

        self._staff_thing_table: List[SoPHueStaffThing] = []
        self._conf_file_path = conf_file_path
        self._conf_select = conf_select

        if self._conf_file_path and '' not in [endpoint_host, api_token]:
            self._endpoint_host = endpoint_host.rstrip('/')
            self._api_token = api_token
            self._header = self._make_header(self._api_token)
        else:
            self._load_config()

        self._endpoint_scan_light = f'{self._endpoint_host}/{self._api_token}/lights'
        # %s: light_id
        self._endpoint_get_light = f'{self._endpoint_host}/{self._api_token}/lights/%s'
        # %s: light_id
        self._endpoint_execute_light = f'{self._endpoint_host}/{self._api_token}/lights/%s/state'
        self._endpoint_scan_sensor = f'{self._endpoint_host}/{self._api_token}/sensors'
        # %s: sensor_id
        self._endpoint_get_sensor = f'{self._endpoint_host}/{self._api_token}/sensors/%s'

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
                        if current_time - staff_thing._last_alive_time > self._alive_cycle:
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
        staff_thing_info_list: dict = API_request(
            self._endpoint_scan_light, RequestMethod.GET, self._header)
        staff_thing_info_list: dict = API_request(
            self._endpoint_scan_light, RequestMethod.GET, self._header)
        if verify_hue_request_result(staff_thing_info_list):
            self._last_scan_time = get_current_time()
            staff_thing_info_list = [dict(idx=idx, staff_thing_info=staff_thing_info)
                                     for idx, staff_thing_info in staff_thing_info_list.items()]
            return staff_thing_info_list
        else:
            return False

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
    def _publish_staff_message(self, staff_msg) -> None:
        pass

    # override
    def _parse_staff_message(self, staff_msg) -> Tuple[SoPProtocolType, str, str]:
        protocol = staff_msg['protocol']
        device_id = staff_msg['device_id']
        payload = staff_msg['payload']

        return protocol, device_id, payload

    # override

    def _create_staff(self, staff_thing_info) -> SoPHueStaffThing:
        idx = int(staff_thing_info['idx'])
        staff_thing_info = staff_thing_info['staff_thing_info']
        name = staff_thing_info['name'].split(
            '(')[0].rstrip().replace(' ', '_')
        # name: str = staff_thing_info['name']
        uniqueid = staff_thing_info['uniqueid']
        type = staff_thing_info['type']
        productname = staff_thing_info['productname']

        if productname == 'Hue color lamp':
            hue_staff_thing = SoPHueColorLampStaffThing(
                name=name, idx=idx, uniqueid=uniqueid, device_id=uniqueid,
                light_function_service_func=self._light_function_service_func, light_value_service_func=self._light_value_service_func)
        elif productname == 'Hue go':
            hue_staff_thing = SoPHueGoStaffThing(
                name=name, idx=idx, uniqueid=uniqueid, device_id=uniqueid,
                light_function_service_func=self._light_function_service_func, light_value_service_func=self._light_value_service_func)
        elif productname == 'Hue lightstrip plus':
            hue_staff_thing = SoPHueLightStripPlusStaffThing(
                name=name, idx=idx, uniqueid=uniqueid, device_id=uniqueid,
                light_function_service_func=self._light_function_service_func, light_value_service_func=self._light_value_service_func)
        elif productname == 'Hue motion sensor':
            pass
        elif productname == 'Hue tap switch':
            pass

        hue_staff_thing.make_service_list()
        hue_staff_thing.set_function_result_queue(self._publish_queue)
        for staff_service in hue_staff_thing.get_value_list() + hue_staff_thing.get_function_list():
            staff_service.add_tag(SoPTag(self._conf_select))

        return hue_staff_thing

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
        staff_thing._staff_registered = False

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

    ############################################################################################################################

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
        room_list = conf_file['room_list']

        for room in room_list:
            room_name = room['name']
            if room_name == conf_select:
                endpoint_host = room['endpoint_host']
                api_token = room['api_token']
                return endpoint_host, api_token

        return False

    def _make_header(self, api_token: str):
        header = SoPHueManagerThing.API_HEADER_TEMPLATE
        header['Authorization'] = header['Authorization'] + api_token
        return header

    ##############################################################################################################################

    def _light_value_service_func(self, idx: int, action: HueLightAction) -> bool:
        endpoint_get_light = self._endpoint_get_light
        header = self._header

        if action == HueLightAction.STATUS:
            light_ret: requests.Response = API_request(
                method=RequestMethod.GET,
                url=endpoint_get_light % idx,
                header=header)
            return light_ret

    def _light_function_service_func(self, idx: int, action: HueLightAction, brightness: int = None, color: Tuple[int, int, int] = None) -> bool:
        endpoint_execute = self._endpoint_execute_light
        header = self._header

        if action == HueLightAction.ON:
            ret: requests.Response = API_request(
                method=RequestMethod.PUT,
                url=endpoint_execute % idx,
                body=dict_to_json_string({'on': True}),
                header=header)
        elif action == HueLightAction.OFF:
            ret: requests.Response = API_request(
                method=RequestMethod.PUT,
                url=endpoint_execute % idx,
                body=dict_to_json_string({'on': False}),
                header=header)
        elif action == HueLightAction.BRIGHTNESS:
            if not isinstance(brightness, tuple):
                raise Exception('brightness must be tuple type')
            ret: requests.Response = API_request(
                method=RequestMethod.PUT,
                url=endpoint_execute % idx,
                body=dict_to_json_string({'bri': brightness}),
                header=self._header)
        elif action == HueLightAction.COLOR:
            if not isinstance(color, tuple):
                raise Exception('color must be tuple type')
            x, y = rgb_to_xy(*color)
            ret: requests.Response = API_request(
                method=RequestMethod.PUT,
                url=endpoint_execute % idx,
                body=dict_to_json_string({'xy': [x, y]}),
                header=self._header)
        elif action == HueLightAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.PUT,
                url=endpoint_execute % idx,
                body=dict_to_json_string({'xy': [x, y]}),
                header=self._header)

        verify_result = verify_hue_request_result(ret)
        if verify_result:
            data = ret.json()
            if 'success' in data[0]:
                return True
            else:
                return False
        else:
            return False
