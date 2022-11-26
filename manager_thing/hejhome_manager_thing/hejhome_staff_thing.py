from big_thing_py.manager_thing import *
from hejhome_utils import *


class SoPHejhomeStaffThing(SoPStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 device_id: str = '',
                 id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id)
        self.id = id
        self.home_name = home_name
        self.home_id = home_id
        self.room_name = room_name
        self.room_id = room_id
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func
        
        self._default_tag_list: List[SoPTag] = [SoPTag(self._name),
                                                SoPTag(self.id),
                                                SoPTag(self.home_name),
                                                SoPTag(self.room_name),
                                                SoPTag('Hejhome')]

    @SoPStaffThing.print_func_info
    def get_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        

    def add_tag_to_service(self, service_list: List[SoPService]):
        for staff_service in service_list:
            for tag in self._default_tag_list:
                staff_service.add_tag(tag)
            self._add_service(staff_service)

    # override
    def make_service_list(self):
        staff_value_list = []
        staff_function_list = [SoPFunction(name='state',
                                         func=self.get_state,
                                         return_type=SoPType.STRING,
                                         arg_list=[],
                                         exec_time=10000,
                                         timeout=10000)]
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPBruntPlugHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        on_state = ret['deviceState']['power']
        return on_state

    @SoPStaffThing.print_func_info
    def get_current(self):
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curCurrent'])
    
    @SoPStaffThing.print_func_info
    def get_power(self):
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curPower']) / 10
    
    @SoPStaffThing.print_func_info
    def get_voltage(self):
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curVoltage']) / 10

    # override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPValue(name='is_on',
                                    func=self.is_on,
                                    type=SoPType.BOOL,
                                    bound=(0, 2),
                                    cycle=60),
                            SoPValue(name='current',
                                    func=self.get_current,
                                    type=SoPType.DOUBLE,
                                    bound=(0, 100000),
                                    cycle=60),
                            SoPValue(name='power',
                                    func=self.get_power,
                                    type=SoPType.DOUBLE,
                                    bound=(0, 100000),
                                    cycle=60),
                            SoPValue(name='voltage',
                                    func=self.get_voltage,
                                    type=SoPType.DOUBLE,
                                    bound=(0, 100000),
                                    cycle=60)]
        staff_function_list: List[SoPService] = []
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPCurtainHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_onen(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)

        open_state:str = ret['deviceState']['workState']
        if open_state.lower() == 'open':
            return True
        elif open_state.lower() == 'close':
            return False
    
    @SoPStaffThing.print_func_info
    def get_curtain_open_percent(self) -> int:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        open_percent = int(ret['deviceState']['percentState'])
        return open_percent

    @SoPStaffThing.print_func_info
    def curtain_open(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.CURTAIN_OPEN)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def curtain_close(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.CURTAIN_CLOSE)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def curtain_open_control(self, percent: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.CURTAIN_CONTROL, curtain_percent=percent)
        if ret:
            return True
        else:
            return False

    # override
    def make_service_list(self):
        super().make_service_list()
        
        staff_value_list = [SoPValue(name='is_onen',
                                    func=self.is_onen,
                                    type=SoPType.BOOL,
                                    bound=(0, 2),
                                    cycle=60),
                            SoPValue(name='curtain_open_percent',
                                    func=self.get_curtain_open_percent,
                                    type=SoPType.INTEGER,
                                    bound=(0, 100),
                                    cycle=60),]
        staff_function_list = [SoPFunction(name='curtain_open',
                                         func=self.curtain_open,
                                         return_type=SoPType.BOOL,
                                         arg_list=[],
                                         exec_time=10000,
                                         timeout=10000),
                               SoPFunction(name='curtain_close',
                                         func=self.curtain_close,
                                         return_type=SoPType.BOOL,
                                         arg_list=[],
                                         exec_time=10000,
                                         timeout=10000),
                               SoPFunction(name='curtain_open_control',
                                         func=self.curtain_open_control,
                                         return_type=SoPType.BOOL,
                                         arg_list=[SoPArgument(name='curtain_open_percent',
                                                                type=SoPType.INTEGER,
                                                                bound=(0, 100))],
                                         exec_time=10000,
                                         timeout=10000)]
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPZigbeeSwitch3HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)

        for power, on_state in ret['deviceState'].items():
            if on_state:
                return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def get_sw_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        on_state = dict_to_json_string(ret['deviceState'])
        return on_state

    @SoPStaffThing.print_func_info
    def on_all(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_ON)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def off_all(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_OFF)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def set_sw(self, sw1, sw2, sw3) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_CONTROL, zb_sw=(sw1, sw2, sw3))
        if ret:
            return True
        else:
            return False

    # override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPValue(name='is_on',
                                    func=self.is_on,
                                    type=SoPType.BOOL,
                                    bound=(0, 2),
                                    cycle=60),
                            SoPValue(name='sw_state',
                                  func=self.get_sw_state,
                                  type=SoPType.STRING,
                                  bound=(0, 100),
                                  cycle=60)]

        staff_function_list = [SoPFunction(name='on_all',
                                      func=self.on_all,
                                      return_type=SoPType.BOOL,
                                      arg_list=[],
                                      exec_time=10000,
                                      timeout=10000),
                               SoPFunction(name='off_all',
                                       func=self.off_all,
                                       return_type=SoPType.BOOL,
                                       arg_list=[],
                                       exec_time=10000,
                                       timeout=10000),
                               SoPFunction(name='set_sw',
                                   func=self.set_sw,
                                   return_type=SoPType.BOOL,
                                   arg_list=[SoPArgument(name='sw1',
                                                         type=SoPType.BOOL,
                                                         bound=(0, 2)),
                                             SoPArgument(name='sw2',
                                                         type=SoPType.BOOL,
                                                         bound=(0, 2)),
                                             SoPArgument(name='sw3',
                                                         type=SoPType.BOOL,
                                                         bound=(0, 2))],
                                   exec_time=10000,
                                   timeout=10000)]
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPIrDiyHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        super().make_service_list()


class SoPIrAirconditionerHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    # override
    def make_service_list(self):
        super().make_service_list()


class SoPLedStripRgbw2HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        on_state = ret['deviceState']['power']
        return on_state
    
    @SoPStaffThing.print_func_info
    def get_brightness(self) -> int:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        brightness = ret['deviceState']['brightness']
        return brightness
    
    @SoPStaffThing.print_func_info
    def get_color(self) -> str:
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        color = ret['deviceState']['hsvColor']
        return dict_to_json_string(color)
    
    @SoPStaffThing.print_func_info
    def on(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ON)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def off(self) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.OFF)
        if ret:
            return True
        else:
            return False
    
    @SoPStaffThing.print_func_info
    def set_brightness(self, brightness: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.BRIGHTNESS, brightness=brightness)
        if ret:
            return True
        else:
            return False
    
    @SoPStaffThing.print_func_info
    def set_color(self, r: int, g: int, b: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.COLOR, color=(r, g, b))
        if ret:
            return True
        else:
            return False

    # override
    def make_service_list(self):
        super().make_service_list()
        
        staff_value_list = [SoPValue(name='is_on',
                                    func=self.is_on,
                                    type=SoPType.BOOL,
                                    bound=(0, 2),
                                    cycle=60),
                            SoPValue(name='brightness',
                                  func=self.get_brightness,
                                  type=SoPType.STRING,
                                  bound=(0, 100),
                                  cycle=60),
                            SoPValue(name='color',
                                  func=self.get_color,
                                  type=SoPType.STRING,
                                  bound=(0, 100),
                                  cycle=60)
                            ]
        staff_function_list = [SoPFunction(name='on',
                                      func=self.on,
                                      return_type=SoPType.BOOL,
                                      arg_list=[],
                                      exec_time=10000,
                                      timeout=10000),
                               SoPFunction(name='off',
                                       func=self.off,
                                       return_type=SoPType.BOOL,
                                       arg_list=[],
                                       exec_time=10000,
                                       timeout=10000),
                               SoPFunction(name='set_brightness',
                                      func=self.set_brightness,
                                      return_type=SoPType.BOOL,
                                      arg_list=[SoPArgument(name='brightness',
                                                            type=SoPType.INTEGER,
                                                            bound=(0, 255))],
                                      exec_time=10000,
                                      timeout=10000),
                               SoPFunction(name='set_color',
                                       func=self.set_color,
                                       return_type=SoPType.BOOL,
                                       arg_list=[SoPArgument(name='r',
                                                            type=SoPType.INTEGER,
                                                            bound=(0, 255)),
                                                SoPArgument(name='g',
                                                            type=SoPType.INTEGER,
                                                            bound=(0, 255)),
                                                SoPArgument(name='b',
                                                            type=SoPType.INTEGER,
                                                            bound=(0, 255))],
                                       exec_time=10000,
                                       timeout=10000)]
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPIrTvHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        return super().make_service_list()


class SoPRadarPIRSensorHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None,
                 pir_status_timeout: float = 5.0):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)
        self._pir_status: dict = {}
        self._pir_status_timeout = pir_status_timeout

    @SoPStaffThing.print_func_info
    def get_pir_state(self) -> bool:
        current_time = get_current_time()
        if self._pir_status:
            if current_time - self._pir_status['t']/1000 > self._pir_status_timeout:
                return False
            else:
                return True
        else:
            return False

    # override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPValue(name='pir_state',
                                   func=self.get_pir_state,
                                   type=SoPType.BOOL,
                                   bound=(0, 2),
                                   cycle=self._pir_status_timeout / 2)]
        staff_function_list = []
        self.add_tag_to_service(staff_value_list + staff_function_list)
            