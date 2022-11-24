from big_thing_py.manager_thing import *
from hue_utils import *


class SoPHueStaffThing(SoPStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True,
                 device_id: str = None, idx: int = None, uniqueid: str = '',
                 light_function_service_func: Callable = None, light_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, device_id)
        self.idx = idx
        self.uniqueid = uniqueid
        self._light_function_service_func = light_function_service_func
        self._light_value_service_func = light_value_service_func

    def is_on(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        on_state = ret['state']['on']
        return on_state

    def get_brightness(self) -> int:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        bri_state = int(ret['state']['bri'])
        return bri_state

    def get_state(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        state = ret['state']
        return state

    def on(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.ON)
        return ret

    def off(self) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.OFF)
        return ret

    def make_service_list(self):
        on_value = SoPValue(name='is_on',
                            func=self.is_on,
                            type=type_converter(get_function_return_type(
                                self.is_on)),
                            bound=(0, 2),
                            cycle=5)
        brightness_value = SoPValue(name='get_brightness',
                                    func=self.get_brightness,
                                    type=type_converter(get_function_return_type(
                                        self.get_brightness)),
                                    bound=(0, 256),
                                    cycle=5)
        on_function = SoPFunction(name='on',
                                  func=self.on,
                                  return_type=type_converter(
                                      get_function_return_type(self.on)),
                                  arg_list=[],
                                  exec_time=10000,
                                  timeout=10000)
        off_function = SoPFunction(name='off',
                                   func=self.off,
                                   return_type=type_converter(
                                        get_function_return_type(self.off)),
                                   arg_list=[],
                                   exec_time=10000,
                                   timeout=10000)
        get_state_function = SoPFunction(name='state',
                                         func=self.get_state,
                                         return_type=type_converter(
                                             get_function_return_type(self.get_state)),
                                         arg_list=[],
                                         exec_time=10000,
                                         timeout=10000)

        staff_function_list: List[SoPService] = [on_function,
                                                 off_function]
        staff_value_list: List[SoPService] = [on_value,
                                              brightness_value,
                                              get_state_function]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.uniqueid))
            staff_service.add_tag(SoPTag('Hue'))
            self._add_service(staff_service)


class SoPHueColorLampStaffThing(SoPHueStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', light_function_service_func: Callable = None, light_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, light_function_service_func, light_value_service_func)

    def get_color(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        color = xy_to_rgb(*tuple(ret['state']['xy'] + [ret['state']['bri']]))
        color_state = f'r:{color[0]}, g:{color[1]}, b:{color[2]}'
        return color_state

    def set_brightness(self, brightness: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, brightness)
        return ret

    def set_color(self, r: int, g: int, b: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, (r, g, b))
        return ret

    def make_service_list(self):
        super().make_service_list()

        color_value = SoPValue(name='get_color',
                                    func=self.get_color,
                                    type=type_converter(get_function_return_type(
                                        self.get_color)),
                                    bound=(0, 100),
                                    cycle=5)
        set_brightness_function = SoPFunction(name='set_brightness',
                                              func=self.set_brightness,
                                              return_type=type_converter(
                                                  get_function_return_type(self.set_brightness)),
                                              arg_list=[SoPArgument(name='brightness',
                                                                    type=SoPType.INTEGER,
                                                                    bound=(0, 255))],
                                              exec_time=10000,
                                              timeout=10000)
        set_color_function = SoPFunction(name='set_color',
                                         func=self.set_color,
                                         return_type=type_converter(
                                             get_function_return_type(self.set_color)),
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
                                         timeout=10000)

        staff_function_list: List[SoPService] = [set_brightness_function,
                                                 set_color_function]
        staff_value_list: List[SoPService] = [color_value]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.uniqueid))
            staff_service.add_tag(SoPTag('Hue'))
            self._add_service(staff_service)


class SoPHueGoStaffThing(SoPHueStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', light_function_service_func: Callable = None, light_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, light_function_service_func, light_value_service_func)

    def get_color(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        color = xy_to_rgb(*tuple(ret['state']['xy'] + [ret['state']['bri']]))
        color_state = f'r:{color[0]}, g:{color[1]}, b:{color[2]}'
        return color_state

    def set_brightness(self, brightness: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, brightness)
        return ret

    def set_color(self, r: int, g: int, b: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, (r, g, b))
        return ret

    def make_service_list(self):
        super().make_service_list()

        color_value = SoPValue(name='get_color',
                                    func=self.get_color,
                                    type=type_converter(get_function_return_type(
                                        self.get_color)),
                                    bound=(0, 100),
                                    cycle=5)
        set_brightness_function = SoPFunction(name='set_brightness',
                                              func=self.set_brightness,
                                              return_type=type_converter(
                                                  get_function_return_type(self.set_brightness)),
                                              arg_list=[SoPArgument(name='brightness',
                                                                    type=SoPType.INTEGER,
                                                                    bound=(0, 255))],
                                              exec_time=10000,
                                              timeout=10000)
        set_color_function = SoPFunction(name='set_color',
                                         func=self.set_color,
                                         return_type=type_converter(
                                             get_function_return_type(self.set_color)),
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
                                         timeout=10000)

        staff_function_list: List[SoPService] = [set_brightness_function,
                                                 set_color_function]
        staff_value_list: List[SoPService] = [color_value]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.uniqueid))
            staff_service.add_tag(SoPTag('Hue'))
            self._add_service(staff_service)


class SoPHueLightStripPlusStaffThing(SoPHueStaffThing):
    def __init__(self, name: str, service_list: List[SoPService] = None, alive_cycle: float = 10, is_super: bool = False, is_parallel: bool = True, device_id: str = None, idx: int = None, uniqueid: str = '', light_function_service_func: Callable = None, light_value_service_func: Callable = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         device_id, idx, uniqueid, light_function_service_func, light_value_service_func)

    def get_color(self) -> str:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret: requests.Response = self._light_value_service_func(
            self.idx, HueLightAction.STATUS)
        color = xy_to_rgb(*tuple(ret['state']['xy'] + [ret['state']['bri']]))
        color_state = f'r:{color[0]}, g:{color[1]}, b:{color[2]}'
        return color_state

    def set_brightness(self, brightness: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, brightness)
        return ret

    def set_color(self, r: int, g: int, b: int) -> bool:
        SOPLOG_DEBUG(
            f'{get_current_function_name()} at {self._name} actuate!!!', 'green')
        ret = self._light_function_service_func(
            self.idx, HueLightAction.BRIGHTNESS, (r, g, b))
        return ret

    def make_service_list(self):
        super().make_service_list()

        color_value = SoPValue(name='get_color',
                                    func=self.get_color,
                                    type=type_converter(get_function_return_type(
                                        self.get_color)),
                                    bound=(0, 100),
                                    cycle=5)
        set_brightness_function = SoPFunction(name='set_brightness',
                                              func=self.set_brightness,
                                              return_type=type_converter(
                                                  get_function_return_type(self.set_brightness)),
                                              arg_list=[SoPArgument(name='brightness',
                                                                    type=SoPType.INTEGER,
                                                                    bound=(0, 255))],
                                              exec_time=10000,
                                              timeout=10000)
        set_color_function = SoPFunction(name='set_color',
                                         func=self.set_color,
                                         return_type=type_converter(
                                             get_function_return_type(self.set_color)),
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
                                         timeout=10000)

        staff_function_list: List[SoPService] = [set_brightness_function,
                                                 set_color_function]
        staff_value_list: List[SoPService] = [color_value]
        service_list: List[SoPService] = staff_function_list + staff_value_list
        for staff_service in service_list:
            staff_service.add_tag(SoPTag(self._name))
            staff_service.add_tag(SoPTag(self.uniqueid))
            staff_service.add_tag(SoPTag('Hue'))
            self._add_service(staff_service)
