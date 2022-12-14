from big_thing_py.manager_thing import *
from hue_utils import *


class SoPHueStaffThing(SoPStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True,
                 device_id: str = None, idx: int = None, uniqueid: str = '',
                 device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id)
        self.idx = idx
        self.uniqueid = uniqueid
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func

        self._default_tag_list: List[SoPTag] = [SoPTag(self._name),
                                                SoPTag(self.uniqueid),
                                                SoPTag('Hue')]

    @SoPStaffThing.print_func_info
    def get_state(self) -> str:
        ret: requests.Response = self._device_value_service_func(
            self.idx, HueLightAction.STATUS)
        state = ret['state']
        return state

    @SoPStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(
            self.idx, HueLightAction.STATUS)
        on_state = ret['state']['on']
        return on_state

    @SoPStaffThing.print_func_info
    def get_brightness(self) -> int:
        ret: requests.Response = self._device_value_service_func(
            self.idx, HueLightAction.STATUS)
        bri_state = int(ret['state']['bri'])
        return bri_state

    @SoPStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(
            self.idx, HueLightAction.ON)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(
            self.idx, HueLightAction.OFF)
        if ret:
            return True
        else:
            return False

    def add_tag_to_service(self, service_list: List[SoPService]):
        for staff_service in service_list:
            for tag in self._default_tag_list:
                staff_service.add_tag(tag)
            self._add_service(staff_service)

    # override
    def make_service_list(self):
        staff_value_list = [SoPValue(name='is_on',
                                     func=self.is_on,
                                     type=SoPType.BOOL,
                                     bound=(0, 2),
                                     cycle=5),
                            SoPValue(name='get_brightness',
                                     func=self.get_brightness,
                                     type=SoPType.INTEGER,
                                     bound=(0, 256),
                                     cycle=5),
                            SoPFunction(name='on',
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
        staff_function_list = [SoPFunction(name='state',
                                           func=self.get_state,
                                           return_type=SoPType.STRING,
                                           arg_list=[],
                                           exec_time=10000,
                                           timeout=10000)]
        self.add_tag_to_service(staff_value_list + staff_function_list)


class SoPHueColorStaffThing(SoPHueStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, device_function_service_func, device_value_service_func)

    @SoPStaffThing.print_func_info
    def get_color(self) -> str:
        ret: requests.Response = self._device_value_service_func(
            self.idx, HueLightAction.STATUS)
        color = xy_to_rgb(*tuple(ret['state']['xy'] + [ret['state']['bri']]))
        color_state = f'r:{color[0]}, g:{color[1]}, b:{color[2]}'
        return color_state

    @SoPStaffThing.print_func_info
    def set_brightness(self, brightness: int) -> bool:
        ret = self._device_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, brightness)
        if ret:
            return True
        else:
            return False

    @SoPStaffThing.print_func_info
    def set_color(self, r: int, g: int, b: int) -> bool:
        ret = self._device_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, (r, g, b))
        if ret:
            return True
        else:
            return False

    # override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [SoPValue(name='get_color',
                                     func=self.get_color,
                                     type=SoPType.STRING,
                                     bound=(0, 100),
                                     cycle=5)]
        staff_function_list = [SoPFunction(name='set_brightness',
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


class SoPHueColorLampStaffThing(SoPHueColorStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, device_function_service_func, device_value_service_func)

    # override
    def make_service_list(self):
        super().make_service_list()


class SoPHueGoStaffThing(SoPHueColorStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, device_function_service_func, device_value_service_func)

    # override
    def make_service_list(self):
        super().make_service_list()


class SoPHueLightStripPlusStaffThing(SoPHueColorStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', device_function_service_func: Callable = None, device_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, device_function_service_func, device_value_service_func)

    # override
    def make_service_list(self):
        super().make_service_list()
