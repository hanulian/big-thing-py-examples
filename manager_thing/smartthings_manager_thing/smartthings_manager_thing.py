from big_thing_py.poll_manager_thing import *
from smartthings_staff_thing import *
from smartthings_utils import *


class MXSmartThingsManagerThing(MXPollManagerThing):
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

        self._staff_thing_list: List[MXSmartThingsStaffThing] = []
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

        self._endpoint_scan_location = f'{self._endpoint_host}/locations'
        self._endpoint_scan_room = f'{self._endpoint_host}/locations/%s/rooms'
        self._endpoint_scan_device = f'{self._endpoint_host}/devices'
        self._endpoint_get_device_detail_info = f'{self._endpoint_host}/devices/%s'
        self._endpoint_get_device_state = f'{self._endpoint_host}/devices/%s/status'
        self._endpoint_device_control = f'{self._endpoint_host}/devices/%s/commands'

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

    def _scan_staff_thing(self, timeout: float = 10) -> List[dict]:
        staff_thing_info_list = []

        whole_location_info = dict(location_list=[])
        res = API_request(
            url=self._endpoint_scan_location,
            method=RequestMethod.GET,
            header=self._header,
            timeout=timeout,
        )
        if not res:
            MXLOG_DEBUG(f'Failed to get location info', 'red')
            return False
        location_list = res['items']
        for location in location_list:
            location_info = dict(name=location['name'], id=location['locationId'], room_list=[])
            res = API_request(
                url=self._endpoint_scan_room % location['locationId'],
                method=RequestMethod.GET,
                header=self._header,
                timeout=timeout,
            )
            if not res:
                raise Exception('Failed to get room info')
            room_list = res['items']
            for room in room_list:
                room_info = dict(name=room['name'], id=room['roomId'], device_list=[])
                location_info['room_list'].append(room_info)
            whole_location_info['location_list'].append(location_info)

        res = API_request(
            url=self._endpoint_scan_device,
            method=RequestMethod.GET,
            header=self._header,
            timeout=timeout,
        )
        if not res:
            MXLOG_DEBUG(f'Failed to get device info', 'red')
            return False
        device_list = res['items']
        # device type candidate: ['OCF', 'VIPER', 'MOBILE']
        device_list = [device for device in device_list if device['type'] != 'MOBILE']

        for device in device_list:
            for location in whole_location_info['location_list']:
                location_name = location['name']
                location_id = location['id']
                for room in location['room_list']:
                    room_name = room['name']
                    room_id = room['id']
                    if device.get('roomId', None) == room_id and device.get('locationId', None):
                        device['location_name'] = location_name
                        device['room_name'] = room_name
                        room['device_list'].append(device)

        staff_thing_info_list = device_list
        return staff_thing_info_list

    def _create_staff(self, staff_thing_info: dict) -> MXSmartThingsStaffThing:
        trans = str.maketrans({' ': '_', '(': '_', ')': '_', '[': '_', ']': '_', '-': '_'})

        def remove_non_ascii(input_str: str) -> str:
            return ''.join(ch for ch in input_str if ord(ch) < 128)

        location_name = remove_non_ascii(staff_thing_info.get('location_name', '').translate(trans))
        location_id = remove_non_ascii(staff_thing_info.get('locationId', '').translate(trans))
        room_name = remove_non_ascii(staff_thing_info.get('room_name', '').translate(trans))
        room_id = remove_non_ascii(staff_thing_info.get('roomId', '').translate(trans))
        name = remove_non_ascii(staff_thing_info['name'].translate(trans))
        staff_thing_id = staff_thing_info['deviceId']
        label = remove_non_ascii(staff_thing_info['label'].translate(trans))
        type = staff_thing_info['type']
        device_type_name = staff_thing_info.get('deviceTypeName', '')

        component_list = staff_thing_info.get('components', [])
        main_component = [component for component in component_list if component['id'] == 'main'][0]
        capabilities = main_component['capabilities']
        category_list = main_component['categories']
        category = category_list[0]['name']

        label = convert_to_valid_string(label)
        if category == 'AirPurifier':
            smartthings_staff_thing = MXAirPurifierSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'BluetoothTracker':
            smartthings_staff_thing = MXBluetoothTrackerSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'Charger':
            smartthings_staff_thing = MXChargerSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'Hub':
            smartthings_staff_thing = MXHubSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'Light':
            smartthings_staff_thing = MXLightSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'RobotCleaner':
            smartthings_staff_thing = MXRobotCleanerSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'SmartLock':
            smartthings_staff_thing = MXSmartLockSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'SmartPlug':
            smartthings_staff_thing = MXSmartPlugSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'Switch':
            smartthings_staff_thing = MXSwitchSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        elif category == 'Television':
            smartthings_staff_thing = MXTelevisionSmartThingsStaffThing(
                name=label,
                service_list=[],
                alive_cycle=self._alive_cycle,
                staff_thing_id=staff_thing_id,
                label=label,
                location_name=location_name,
                location_id=location_id,
                room_name=room_name,
                room_id=room_id,
                device_type=category,
                device_function_service_func=self._device_function_service_func,
                device_value_service_func=self._device_value_service_func,
            )
        else:
            MXLOG_DEBUG(f'Unexpected category!!! - {category}', 'red')
            return False

        # if not smartthings_staff_thing:
        #     MXLOG_DEBUG(f'Unexpected device type!!! - {device_type_name}', 'red')
        #     # raise Exception('Unexpected device type!!!')
        #     return False

        smartthings_staff_thing.make_service_list()
        smartthings_staff_thing.set_function_result_queue(self._publish_queue)
        for staff_service in smartthings_staff_thing.get_value_list() + smartthings_staff_thing.get_function_list():
            staff_service.add_tag(MXTag(self._conf_select))

        return smartthings_staff_thing

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

            self._endpoint_host, self._api_token = self._extract_info_from_config(conf_file, self._conf_select)
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
                return endpoint_host, api_token

        return False

    def _make_header(self, api_token: str):
        header = MXSmartThingsManagerThing.API_HEADER_TEMPLATE
        header['Authorization'] = header['Authorization'] + api_token
        return header

    ##############################################################################################################################

    def _device_value_service_func(self, staff_thing_id: str, action: SmartThingsAction) -> dict:
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == SmartThingsAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET, url=endpoint_get_device_state % staff_thing_id, header=header
            )
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False

    # TODO: smartthings는 각 디바이스에 대한 커맨드목록을 제공한다. 이를 통해 미리 action을 정의 하지않고도 커맨드를 날릴 수 있다.
    # TODO: 현재는 action을 미리 정의해서 사용하는 방식으로 구현하였다. 나중에 위의 방법으로 바꾸어야함.
    def _device_function_service_func(self, staff_thing_id: str, action: SmartThingsAction) -> dict:
        endpoint_device_control = self._endpoint_device_control
        endpoint_get_device_state = self._endpoint_get_device_state
        header = self._header

        if action == SmartThingsAction.ON:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string(
                    {"commands": [{"component": "main", "capability": "switch", "command": "on", 'arguments': []}]}
                ),
                header=header,
            )
        elif action == SmartThingsAction.OFF:
            ret: requests.Response = API_request(
                method=RequestMethod.POST,
                url=endpoint_device_control % staff_thing_id,
                body=dict_to_json_string(
                    {"commands": [{"component": "main", "capability": "switch", "command": "off", 'arguments': []}]}
                ),
                header=header,
            )
        elif action == SmartThingsAction.STATUS:
            ret: requests.Response = API_request(
                method=RequestMethod.GET, url=endpoint_get_device_state % staff_thing_id, header=self._header
            )
        else:
            raise Exception('invalid action')

        if ret:
            return ret
        else:
            return False
