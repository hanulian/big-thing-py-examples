from big_thing_py.poll_manager_thing import *
from hue_staff_thing import *
from hue_utils import *


class MXHueManagerThing(MXPollManagerThing):
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
        conf_file_path: str = '',
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

        self._conf_file_path = conf_file_path
        self._conf_select = conf_select

        self._endpoint_host = ''
        self._api_token = ''
        self._header = {}

        if not self._conf_file_path:
            raise Exception('Empty conf file path')
        elif not os.path.exists(self._conf_file_path):
            raise Exception('Invalid conf file path')
        else:
            self._load_config()

        self._endpoint_scan_light = f'{self._endpoint_host}/{self._api_token}/lights'
        self._endpoint_get_light = f'{self._endpoint_host}/{self._api_token}/lights/%s'
        self._endpoint_execute_light = f'{self._endpoint_host}/{self._api_token}/lights/%s/state'

        self._endpoint_scan_sensor = f'{self._endpoint_host}/{self._api_token}/sensors'
        self._endpoint_get_sensor = f'{self._endpoint_host}/{self._api_token}/sensors/%s'
        self._endpoint_execute_sensor = f'{self._endpoint_host}/{self._api_token}/sensors/%s/state'

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    # nothing to add...

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
        staff_thing_info_list: dict = API_request(
            self._endpoint_scan_light, RequestMethod.GET, self._header, verify=False, timeout=timeout
        )
        staff_sensor_thing_info_list: dict = API_request(
            self._endpoint_scan_sensor, RequestMethod.GET, self._header, verify=False, timeout=timeout
        )

        if verify_hue_request_result(staff_thing_info_list) or verify_hue_request_result(staff_sensor_thing_info_list):
            staff_thing_info_list = [
                dict(idx=idx, info=staff_thing_info) for idx, staff_thing_info in staff_thing_info_list.items()
            ]
            staff_sensor_thing_info_list = [
                dict(idx=idx, info=staff_thing_info) for idx, staff_thing_info in staff_sensor_thing_info_list.items()
            ]
            return staff_thing_info_list + staff_sensor_thing_info_list
        else:
            return False

    def _create_staff(self, staff_thing_info) -> Union[MXHueStaffThing, None]:
        trans = str.maketrans({' ': '_', '(': '_', ')': '_', '-': '_'})

        idx = int(staff_thing_info['idx'])
        staff_thing_info: dict = staff_thing_info['info']

        # type = staff_thing_info['type']
        name: str = staff_thing_info['name'].translate(trans)
        # modelid = staff_thing_info['modelid']
        # manufacturername = staff_thing_info['manufacturername']
        productname = staff_thing_info.get('productname', None)
        uniqueid = staff_thing_info.get('uniqueid', self.generate_staff_thing_id())
        # swversion = staff_thing_info['swversion']
        # swconfigid = staff_thing_info['swconfigid']
        # productid = staff_thing_info['productid']

        # state: dict = staff_thing_info['state']
        # swupdate: dict = staff_thing_info['swupdate']
        # capabilities: dict = staff_thing_info['capabilities']
        # config: dict = staff_thing_info['config']

        ALIVE_CYCLE = 10
        if productname == 'Hue color lamp':
            hue_staff_thing = MXHueColorLampStaffThing(
                name=name,
                service_list=[],
                alive_cycle=ALIVE_CYCLE,
                staff_thing_id=uniqueid,
                idx=idx,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif productname == 'Hue go':
            hue_staff_thing = MXHueGoStaffThing(
                name=name,
                service_list=[],
                alive_cycle=ALIVE_CYCLE,
                staff_thing_id=uniqueid,
                idx=idx,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif productname == 'Hue lightstrip plus':
            hue_staff_thing = MXHueLightStripPlusStaffThing(
                name=name,
                service_list=[],
                alive_cycle=ALIVE_CYCLE,
                staff_thing_id=uniqueid,
                idx=idx,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif productname == 'Hue motion sensor':
            hue_staff_thing = MXHueMotionSensorStaffThing(
                name=name,
                service_list=[],
                alive_cycle=ALIVE_CYCLE,
                staff_thing_id=uniqueid,
                idx=idx,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif productname == 'Hue tap switch':
            MXLOG_DEBUG(
                f'Not supported product!!! name: {staff_thing_info["name"]}, type: {staff_thing_info["type"]}',
                'yellow',
            )
        else:
            # FIXME: Add implement for other device type
            MXLOG_DEBUG(
                f'Not supported product!!! name: {staff_thing_info["name"]}, type: {staff_thing_info["type"]}',
                'yellow',
            )
            return None

        hue_staff_thing.make_service_list()
        hue_staff_thing.set_function_result_queue(self._publish_queue)
        for staff_service in hue_staff_thing.get_value_list() + hue_staff_thing.get_function_list():
            staff_service.add_tag(MXTag(self._conf_select))

        return hue_staff_thing

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
            config_list = conf_file['room_list']
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

            self._endpoint_host, self._api_token = self._extract_info_from_config(conf_file, self._conf_select)
            self._header = self._make_header(self._api_token)
        elif self._endpoint_host == '' or self._endpoint_host == None:
            raise Exception('endpoint host is empty. exit program...')
        else:
            raise Exception('config file is empty. exit program...')

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
        header = MXHueManagerThing.API_HEADER_TEMPLATE
        header['Authorization'] = header['Authorization'] + api_token
        return header

    ##############################################################################################################################

    def _device_value_service_func(self, idx: int, device_type: MXHueDeviceType, action: MXHueAction) -> bool:
        light_endpoint = self._endpoint_get_light
        sensor_endpoint = self._endpoint_get_sensor
        header = self._header

        if action == MXHueAction.STATUS:
            if device_type == MXHueDeviceType.LIGHT:
                ret: requests.Response = API_request(
                    method=RequestMethod.GET, url=light_endpoint % idx, header=header, verify=False
                )
            elif device_type == MXHueDeviceType.SENSOR:
                ret: requests.Response = API_request(
                    method=RequestMethod.GET, url=sensor_endpoint % idx, header=header, verify=False
                )
            return ret
        elif action == MXHueAction.IS_ON:
            if device_type == MXHueDeviceType.LIGHT:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.LIGHT, action=MXHueAction.STATUS
                )
                return ret['state']['on']
            elif device_type == MXHueDeviceType.SENSOR:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.SENSOR, action=MXHueAction.STATUS
                )
                return ret['config']['on']
        elif action == MXHueAction.GET_BRIGHTNESS:
            if device_type == MXHueDeviceType.LIGHT:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.LIGHT, action=MXHueAction.STATUS
                )
                return ret['state']['bri']
            elif device_type == MXHueDeviceType.SENSOR:
                raise Exception('sensor does not have brightness')
        elif action == MXHueAction.GET_COLOR:
            if device_type == MXHueDeviceType.LIGHT:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.LIGHT, action=MXHueAction.STATUS
                )
                color = xy_to_rgb(*tuple(ret['state']['xy'] + [ret['state']['bri']]))
                return color
            elif device_type == MXHueDeviceType.SENSOR:
                raise Exception('sensor does not have color')
        elif action == MXHueAction.GET_DAYLIGHT:
            if device_type == MXHueDeviceType.LIGHT:
                raise Exception('light does not have daylight')
            elif device_type == MXHueDeviceType.SENSOR:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.SENSOR, action=MXHueAction.STATUS
                )
                return ret['state']['presence']
        elif action == MXHueAction.GET_MOTION:
            if device_type == MXHueDeviceType.LIGHT:
                raise Exception('light does not have motion')
            elif device_type == MXHueDeviceType.SENSOR:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.SENSOR, action=MXHueAction.STATUS
                )
                return ret['state']['presence']
        elif action == MXHueAction.GET_LIGHTLEVEL:
            if device_type == MXHueDeviceType.LIGHT:
                raise Exception('light does not have lightlevel')
            elif device_type == MXHueDeviceType.SENSOR:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.SENSOR, action=MXHueAction.STATUS
                )
                return ret['state']['lightlevel']
        elif action == MXHueAction.GET_TEMPERATURE:
            if device_type == MXHueDeviceType.LIGHT:
                raise Exception('light does not have temperature')
            elif device_type == MXHueDeviceType.SENSOR:
                ret: dict = self._device_value_service_func(
                    idx=idx, device_type=MXHueDeviceType.SENSOR, action=MXHueAction.STATUS
                )
                return ret['state']['temperature']
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False

    def _device_function_service_func(
        self,
        idx: int,
        device_type: MXHueDeviceType,
        action: MXHueAction,
        brightness: int = None,
        color: Tuple[int, int, int] = None,
    ) -> bool:
        light_endpoint = self._endpoint_execute_light
        header = self._header

        if action == MXHueAction.STATUS:
            if device_type == MXHueDeviceType.LIGHT:
                ret: requests.Response = API_request(
                    method=RequestMethod.GET, url=light_endpoint % idx, header=header, verify=False
                )
            elif device_type == MXHueDeviceType.SENSOR:
                raise Exception('sensor does not have status')
            return ret['state']
        elif action == MXHueAction.ON:
            if device_type == MXHueDeviceType.LIGHT:
                ret: requests.Response = API_request(
                    method=RequestMethod.PUT,
                    url=light_endpoint % idx,
                    body=dict_to_json_string({'on': True}),
                    header=header,
                    verify=False,
                )
        elif action == MXHueAction.OFF:
            if device_type == MXHueDeviceType.LIGHT:
                ret: requests.Response = API_request(
                    method=RequestMethod.PUT,
                    url=light_endpoint % idx,
                    body=dict_to_json_string({'on': False}),
                    header=header,
                    verify=False,
                )
        elif action == MXHueAction.SET_BRIGHTNESS:
            if device_type == MXHueDeviceType.LIGHT:
                if not isinstance(brightness, tuple):
                    raise Exception('brightness must be tuple type')
                ret: requests.Response = API_request(
                    method=RequestMethod.PUT,
                    url=light_endpoint % idx,
                    body=dict_to_json_string({'bri': brightness}),
                    header=header,
                    verify=False,
                )
        elif action == MXHueAction.SET_COLOR:
            if device_type == MXHueDeviceType.LIGHT:
                if not isinstance(color, tuple):
                    raise Exception('color must be tuple type')
                x, y = rgb_to_xy(*color)
                ret: requests.Response = API_request(
                    method=RequestMethod.PUT,
                    url=light_endpoint % idx,
                    body=dict_to_json_string({'xy': [x, y]}),
                    header=header,
                    verify=False,
                )
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False
