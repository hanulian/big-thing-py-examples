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

    def get_state(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)

    def make_service_list(self):
        get_state_function = SoPFunction(name='state',
                                         func=self.get_state,
                                         return_type=type_converter(
                                             get_function_return_type(self.get_state)),
                                         arg_list=[],
                                         exec_time=10000,
                                         timeout=10000)

        staff_value_list: List[SoPService] = []
        staff_function_list: List[SoPService] = [get_state_function]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.id))
            staff_service.add_tag(SoPTag(self.home_name))
            staff_service.add_tag(SoPTag(self.room_name))
            staff_service.add_tag(SoPTag('Hejhome'))
            self._add_service(staff_service)


class SoPBruntPlugHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def is_on(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)
        on_state = ret['deviceState']['power']
        return on_state

    def get_current(self):
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curCurrent'])

    def get_power(self):
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curPower']) / 10

    def get_voltage(self):
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curVoltage']) / 10

    def make_service_list(self):
        super().make_service_list()

        on_value = SoPValue(name='is_on',
                            func=self.is_on,
                            type=type_converter(get_function_return_type(
                                self.is_on)),
                            bound=(0, 2),
                            cycle=60)
        current_value = SoPValue(name='current',
                                 func=self.get_current,
                                 type=SoPType.DOUBLE,
                                 cycle=60)
        power_value = SoPValue(name='power',
                               func=self.get_power,
                               type=SoPType.DOUBLE,
                               cycle=60)
        voltage_value = SoPValue(name='voltage',
                                 func=self.get_voltage,
                                 type=SoPType.DOUBLE,
                                 cycle=60)

        staff_value_list: List[SoPService] = [
            on_value, current_value, power_value, voltage_value]
        staff_function_list: List[SoPService] = []
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.id))
            staff_service.add_tag(SoPTag(self.home_name))
            staff_service.add_tag(SoPTag(self.room_name))
            staff_service.add_tag(SoPTag('Hejhome'))
            self._add_service(staff_service)


class SoPCurtainHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        super().make_service_list()


class SoPZigbeeSwitch3HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def is_on(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_value_service_func(
            self.id, HejHomeAction.STATUS)

        for power, on_state in ret['deviceState'].items():
            if on_state:
                return True
        else:
            return False

    def get_sw_state(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.STATUS)
        on_state = dict_to_json_string(ret['deviceState'])
        return on_state

    def on_all(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_ON)
        if ret:
            return True
        else:
            return False

    def off_all(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_OFF)
        if ret:
            return True
        else:
            return False

    def set(self, sw1, sw2, sw3) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._device_function_service_func(
            self.id, HejHomeAction.ZBSW_CONTROL, zb_sw=(sw1, sw2, sw3))
        if ret:
            return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        on_value = SoPValue(name='is_on',
                            func=self.is_on,
                            type=type_converter(get_function_return_type(
                                self.is_on)),
                            bound=(0, 2),
                            cycle=60)
        sw_state_value = SoPValue(name='sw_state',
                                  func=self.get_sw_state,
                                  type=type_converter(get_function_return_type(
                                      self.get_sw_state)),
                                  bound=(0, 100),
                                  cycle=60)
        on_all_function = SoPFunction(name='on_all',
                                      func=self.on_all,
                                      return_type=type_converter(
                                          get_function_return_type(self.on_all)),
                                      arg_list=[],
                                      exec_time=10000,
                                      timeout=10000)
        off_all_function = SoPFunction(name='off_all',
                                       func=self.off_all,
                                       return_type=type_converter(
                                           get_function_return_type(self.off_all)),
                                       arg_list=[],
                                       exec_time=10000,
                                       timeout=10000)
        set_function = SoPFunction(name='set',
                                   func=self.set,
                                   return_type=type_converter(
                                        get_function_return_type(self.set)),
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
                                   timeout=10000)

        staff_value_list: List[SoPService] = [on_value, sw_state_value]
        staff_function_list: List[SoPService] = [on_all_function,
                                                 off_all_function,
                                                 set_function]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.id))
            staff_service.add_tag(SoPTag(self.home_name))
            staff_service.add_tag(SoPTag(self.room_name))
            staff_service.add_tag(SoPTag('Hejhome'))
            self._add_service(staff_service)


class SoPIrDiyHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        return super().make_service_list()


class SoPIrAirconditionerHejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        return super().make_service_list()


class SoPLedStripRgbw2HejhomeStaffThing(SoPHejhomeStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = '', id: str = '', home_name: str = '', home_id: str = '', room_name: str = '', room_id: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, id,
                         home_name, home_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        return super().make_service_list()


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

    # def is_on(self) -> bool:
    #     SOPLOG_DEBUG(
    #         f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
    #     ret: requests.Response = self._device_value_service_func(
    #         self.id, HejHomeAction.STATUS)
    #     on_state = ret['deviceState']['power']
    #     return on_state

    def get_pir_state(self) -> bool:
        current_time = get_current_time()
        if self._pir_status:
            if current_time - self._pir_status['t']/1000 > self._pir_status_timeout:
                return False
            else:
                return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        # on_value = SoPValue(name='is_on',
        #                     func=self.is_on,
        #                     type=type_converter(get_function_return_type(
        #                         self.is_on)),
        #                     bound=(0, 2),
        #                     cycle=60)
        pir_state_value = SoPValue(name='pir_state',
                                   func=self.get_pir_state,
                                   type=SoPType.BOOL,
                                   bound=(0, 2),
                                   cycle=self._pir_status_timeout / 2)

        staff_value_list: List[SoPService] = [pir_state_value]
        staff_function_list: List[SoPService] = []
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.id))
            staff_service.add_tag(SoPTag(self.home_name))
            staff_service.add_tag(SoPTag(self.room_name))
            staff_service.add_tag(SoPTag('Hejhome'))
            self._add_service(staff_service)
