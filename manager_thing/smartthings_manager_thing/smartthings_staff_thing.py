from big_thing_py.manager_thing import *
from smartthings_utils import *
from big_thing_py.utils.json_util import *


class SoPSmartThingsStaffThing(SoPStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id)

        self._label = label
        self._location_name = location_name
        self._room_name = room_name
        self._location_id = location_id
        self._room_id = room_id
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func

        self._default_tag_list: List[SoPTag] = [SoPTag(self._name),
                                                SoPTag(self._device_id),
                                                SoPTag(self._location_name),
                                                SoPTag(self._location_id),
                                                SoPTag(self._room_name),
                                                SoPTag(self._room_id),
                                                SoPTag(self._label),
                                                SoPTag('SmartThings')]

    @SoPStaffThing.print_func_info
    def get_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(
            self._device_id, SmartThingsAction.STATUS)
        
        return dict_to_json_string(ret)

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


class SoPRobotVacuumSmartThingsStaffThing(SoPSmartThingsStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, label, location_name,
                         location_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self._device_id, SmartThingsAction.STATUS)
        on_state = ret['state']['on']
        return on_state

    @SoPStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.ON)
        if ret:
            return ret
        else:
            return False

    @SoPStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.OFF)
        if ret:
            return ret
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPFunction(name='on',
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
                                        timeout=10000)]
        staff_function_list = []
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPTVSmartThingsStaffThing(SoPSmartThingsStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, label, location_name,
                         location_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self._device_id, SmartThingsAction.STATUS)
        on_state = ret['state']['on']
        return on_state

    @SoPStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.ON)
        if ret:
            return ret
        else:
            return False

    @SoPStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.OFF)
        if ret:
            return ret
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPFunction(name='on',
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
                                        timeout=10000)]
        staff_function_list = []
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPAirPurifierSmartThingsStaffThing(SoPSmartThingsStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, label, location_name,
                         location_id, room_name, room_id, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self._device_id, SmartThingsAction.STATUS)
        on_state = ret['state']['on']
        return on_state

    @SoPStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.ON)
        if ret:
            return ret
        else:
            return False

    @SoPStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(
            self._device_id, SmartThingsAction.OFF)
        if ret:
            return ret
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPFunction(name='on',
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
                                        timeout=10000)]
        staff_function_list = []
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPSmartTagSmartThingsStaffThing(SoPSmartThingsStaffThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, label, location_name,
                         location_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        super().make_service_list()


class SoPNonSmartThingsStaffThing(SoPSmartThingsStaffThing):
    '''
        smartthings 플랫폼에 등록된 타 플랫폼 디바이스 (ex: Hue, google nest 등등..)
    '''

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True, device_id: str = None,
                 label: str = '', location_name: str = '', location_id: str = '', room_name: str = '', room_id: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id, label, location_name,
                         location_id, room_name, room_id, device_function_service_func, device_value_service_func)

    def make_service_list(self):
        super().make_service_list()
