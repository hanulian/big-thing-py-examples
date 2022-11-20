from big_thing_py.manager_thing import *
from hejhome_utils import *


class SoPHejhomeStaffThing(SoPStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 device_id: str = None,
                 bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id)
        self._id = self._device_id
        self._room_id = room_id
        self._home_id = home_id
        self._bridge_ip = bridge_ip.strip('/')
        self._user_key = user_key
        self._header = header
        self._api_fail = False

    def on(self) -> bool:
        SOPLOG_DEBUG('on actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'control/' + self._device_id,
            body=dict_to_json_string({'requirments': {'power': True}}),
            header=self._header,
            login_retry=False)
        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False

    def off(self) -> bool:
        SOPLOG_DEBUG('off actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'control/' + self._device_id,
            body=dict_to_json_string({'requirments': {'power': False}}),
            header=self._header,
            login_retry=False)
        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False


class SoPBruntPlugHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)


class SoPCurtainHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)

    def on(self) -> bool:
        SOPLOG_DEBUG('on actuate!!! -> redirect to curtain_open', 'green')
        self.curtain_open()

    def off(self) -> bool:
        SOPLOG_DEBUG('off actuate!!!  -> redirect to curtain_close', 'green')
        self.curtain_close()

    def curtain_open(self) -> bool:
        SOPLOG_DEBUG('on actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'control/' + self._device_id,
            body=dict_to_json_string(
                {'requirments': {'control': 'open', 'percentControl': 0}}),
            header=self._header,
            login_retry=False)
        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False

    def curtain_close(self) -> bool:
        SOPLOG_DEBUG('off actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'control/' + self._device_id,
            body=dict_to_json_string(
                {'requirments': {'control': 'close', 'percentControl': 0}}),
            header=self._header,
            login_retry=False)
        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False


class SoPZigbeeSwitch3HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)
        self.sw1_status = None
        self.sw2_status = None
        self.sw3_status = None

    def switch1_set(self, on) -> bool:
        SOPLOG_DEBUG('switch_on1 actuate!!!', 'green')

        payload = None
        url = f"https://goqual.io/openapi/control/ebe63735f2ce316932alsq"
        headers = {
            'Authorization': f'bearer {self._user_key}',
            'Content-Type': 'application/json;charset-UTF-8'
        }

        if int(on) == 1:
            if not self.sw1_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power1": True,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw1_status = True
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True
        else:
            if self.sw1_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power1": False,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw1_status = False
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True

        # res: requests.Response = API_request(
        #     method=RequestMethod.POST,
        #     url=self._bridge_ip + 'control/' + self._device_id,
        #     body=payload,
        #     header=self._header,
        #     login_retry=False)
        # if res:
        #     return True
        # else:
        #     SOPLOG_DEBUG(
        #         f'[FUNC ERROR] API_request!!!', 'red')
        #     return False

    def switch2_set(self, on) -> bool:
        SOPLOG_DEBUG('switch_on2 actuate!!!', 'green')

        payload = None
        url = f"https://goqual.io/openapi/control/ebe63735f2ce316932alsq"
        headers = {
            'Authorization': f'bearer {self._user_key}',
            'Content-Type': 'application/json;charset-UTF-8'
        }

        if int(on) == 1:
            if not self.sw2_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power2": True,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw2_status = True
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True
        else:
            if self.sw2_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power2": False,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw2_status = False
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True

        # res: requests.Response = API_request(
        #     method=RequestMethod.POST,
        #     url=self._bridge_ip + 'control/' + self._device_id,
        #     body=payload,
        #     header=self._header,
        #     login_retry=False)
        # if res:
        #     return True
        # else:
        #     SOPLOG_DEBUG(
        #         f'[FUNC ERROR] API_request!!!', 'red')
        #     return False

    def switch3_set(self, on) -> bool:
        SOPLOG_DEBUG('switch_on3 actuate!!!', 'green')

        payload = None
        url = f"https://goqual.io/openapi/control/ebe63735f2ce316932alsq"
        headers = {
            'Authorization': f'bearer {self._user_key}',
            'Content-Type': 'application/json;charset-UTF-8'
        }

        if int(on) == 1:
            if not self.sw3_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power3": True,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw3_status = True
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True
        else:
            if self.sw3_status:
                payload = dict_to_json_string({
                    "requirments": {
                        "power3": False,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw3_status = False
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True

        # res: requests.Response = API_request(
        #     method=RequestMethod.POST,
        #     url=self._bridge_ip + 'control/' + self._device_id,
        #     body=payload,
        #     header=self._header,
        #     login_retry=False)
        # if res:
        #     return True
        # else:
        #     SOPLOG_DEBUG(
        #         f'[FUNC ERROR] API_request!!!', 'red')
        #     return False

    def all_switch_set(self, on) -> bool:
        SOPLOG_DEBUG('all_switch_set actuate!!!', 'green')

        payload = None
        url = self._bridge_ip + '/control/' + self._device_id
        headers = {
            'Authorization': f'bearer {self._user_key}',
            'Content-Type': 'application/json;charset-UTF-8'
        }

        first_update_check = self.sw1_status == None or self.sw2_status == None or self.sw3_status == None
        if int(on) == 1:
            status_check = self.sw1_status == False or self.sw2_status == False or self.sw3_status == False
            if first_update_check or status_check:
                payload = dict_to_json_string({
                    "requirments": {
                        "power1": True,
                        "power2": True,
                        "power3": True,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw1_status = True
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True
        else:
            status_check = self.sw1_status == True or self.sw2_status == True or self.sw3_status == True
            if first_update_check or status_check:
                payload = dict_to_json_string({
                    "requirments": {
                        "power1": False,
                        "power2": False,
                        "power3": False,
                    }
                })
                if requests.request("POST", url, headers=headers, data=payload).ok:
                    self.sw1_status = False
                    return True
                else:
                    SOPLOG_DEBUG('API Failed...', 'red')
                    self._api_fail = True
                    raise
            else:
                SOPLOG_DEBUG('API Request Skip...', 'yellow')
                return True


class SoPIrDiyHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)


class SoPIrAirconditionerHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)


class SoPLedStripRgbw2HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)

    def set_brightness(self, brightness: int) -> bool:
        SOPLOG_DEBUG('set_brightness actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip +
            self._user_key + '/lights/' + self._idx + '/state',
            body=dict_to_json_string(
                {
                    'requirments':
                    {
                        'hsvColor':
                        {
                            'saturation': 100,
                            'brightness': brightness
                        }
                    }
                }),
            header=self._header,
            login_retry=False)
        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False

    # FIXME: define set_color method fit to hejhome
    def set_color(self, r, g, b) -> bool:
        pass
        # SOPLOG_DEBUG('set_color actuate!!!', 'green')
        # x, y = rgb_to_xy(float(r), float(g), float(b))
        # res: requests.Response = API_request(
        #     method=RequestMethod.POST,
        #     url=self._bridge_ip +
        #     self._user_key + '/lights/' + self._idx + '/state',
        #     body=dict_to_json_string({'xy': [x, y]}),
        #     header=self._header,
        #     login_retry=False)
        # if res:
        #     return True
        # else:
        #     SOPLOG_DEBUG(
        #         f'[FUNC ERROR] API_request!!!', 'red')
        #     return False


class SoPIrTvHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)


class SoPRadarPIRSensorHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None, bridge_ip=None, user_key=None, header=None, home_id=None, room_id=None,
                 pir_status_timeout: float = 5.0):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, bridge_ip, user_key, header, home_id, room_id)
        self._pir_status: dict = []
        self._pir_status_timeout = pir_status_timeout

    def get_pir_status(self) -> bool:
        current_time = get_current_time()
        if current_time - self._pir_status['t']/1000 > self._pir_status_timeout:
            return False
        else:
            return True
