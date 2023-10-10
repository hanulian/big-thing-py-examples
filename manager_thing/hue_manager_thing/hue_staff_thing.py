from big_thing_py.poll_manager_thing import *
from hue_utils import *


class MXHueStaffThing(MXStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, staff_thing_id)
        self.idx = idx
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func

        self._staff_thing_id = self._staff_thing_id.replace(':', '_').replace('-', '_')

        self._default_tag_list: List[MXTag] = [
            MXTag(tag)
            for tag in [
                self._name,
                self._staff_thing_id,
                'Hue',
            ]
            if tag
        ]

    @MXStaffThing.print_func_info
    def get_state(self) -> str:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.STATUS)
        return ret

    @override
    def make_service_list(self):
        staff_value_list = []
        staff_function_list = [
            MXFunction(
                name='state',
                func=self.get_state,
                return_type=MXType.STRING,
                arg_list=[],
                tag_list=self._default_tag_list,
                exec_time=3,
                timeout=3,
            )
        ]
        self.add_staff_service(staff_value_list + staff_function_list)

    @classmethod
    def add_value(cls, *args, **kwargs):
        def decorator(func):
            called = False

            def wrap(self: MXHueStaffThing, *fargs, **fkwargs):
                nonlocal called
                if not called:
                    kwargs = kwargs | dict(tag_list=self._default_tag_list, func=func)
                    value = MXValue(*args, **kwargs)
                    self.add_service(value)
                    called = True
                return func(self, *fargs, **fkwargs)

            return wrap

        return decorator

    @classmethod
    def add_function(cls, *args, **kwargs):
        def decorator(func):
            called = False

            def wrap(self: MXHueStaffThing, *fargs, **fkwargs):
                nonlocal called
                if not called:
                    kwargs = kwargs | dict(tag_list=self._default_tag_list, func=func)
                    function = MXFunction(*args, **kwargs)
                    self.add_service(function)
                    called = True
                return func(self, *fargs, **fkwargs)

            return wrap

        return decorator


class MXHueSensorStaffThing(MXHueStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @MXHueStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.IS_ON)
        return ret

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, type=MXType.BOOL, bound=(0, 2), tag_list=self._default_tag_list, cycle=5
            )
        ]
        staff_function_list = []
        self.add_staff_service(staff_value_list + staff_function_list)


class MXHueColorLightStaffThing(MXHueStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.IS_ON)
        return ret

    @MXStaffThing.print_func_info
    def get_brightness(self) -> int:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.GET_BRIGHTNESS)
        return ret

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.OFF)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def get_color(self) -> str:
        ret: List[float] = self._device_value_service_func(self.idx, MXHueDeviceType.LIGHT, MXHueAction.GET_COLOR)
        color_state = f'r:{ret[0]}, g:{ret[1]}, b:{ret[2]}'
        return color_state

    @MXStaffThing.print_func_info
    def set_color(self, r: int, g: int, b: int) -> bool:
        ret = self._device_function_service_func(
            self.idx, MXHueDeviceType.LIGHT, MXHueAction.SET_COLOR, color=(r, g, b)
        )
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def set_brightness(self, brightness: int) -> bool:
        ret = self._device_function_service_func(
            self.idx, MXHueDeviceType.LIGHT, MXHueAction.SET_BRIGHTNESS, brightness=brightness
        )
        if ret:
            return True
        else:
            return False

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, type=MXType.BOOL, bound=(0, 2), tag_list=self._default_tag_list, cycle=5
            ),
            MXValue(
                name='get_brightness',
                func=self.get_brightness,
                type=MXType.INTEGER,
                bound=(0, 256),
                tag_list=self._default_tag_list,
                cycle=5,
            ),
            MXValue(
                name='get_color',
                func=self.get_color,
                type=MXType.STRING,
                bound=(0, 100),
                tag_list=self._default_tag_list,
                cycle=5,
            ),
        ]
        staff_function_list = [
            MXFunction(
                name='set_brightness',
                func=self.set_brightness,
                return_type=MXType.BOOL,
                arg_list=[MXArgument(name='brightness', type=MXType.INTEGER, bound=(0, 255))],
                tag_list=self._default_tag_list,
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='on',
                func=self.on,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='off',
                func=self.off,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='set_color',
                func=self.set_color,
                return_type=MXType.BOOL,
                arg_list=[
                    MXArgument(name='r', type=MXType.INTEGER, bound=(0, 255)),
                    MXArgument(name='g', type=MXType.INTEGER, bound=(0, 255)),
                    MXArgument(name='b', type=MXType.INTEGER, bound=(0, 255)),
                ],
                tag_list=self._default_tag_list,
                exec_time=3,
                timeout=3,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXHueColorLampStaffThing(MXHueColorLightStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXHueGoStaffThing(MXHueColorLightStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXHueLightStripPlusStaffThing(MXHueColorLightStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXHueMotionSensorStaffThing(MXHueSensorStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = None,
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        idx: int = None,
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            idx,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.IS_ON)
        return ret

    @MXStaffThing.print_func_info
    def get_daylight(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.GET_DAYLIGHT)
        return ret

    @MXStaffThing.print_func_info
    def get_motion(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.GET_MOTION)
        return ret

    @MXStaffThing.print_func_info
    def get_lightlevel(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.GET_LIGHTLEVEL)
        return ret

    @MXStaffThing.print_func_info
    def get_temperature(self) -> bool:
        ret: dict = self._device_value_service_func(self.idx, MXHueDeviceType.SENSOR, MXHueAction.GET_TEMPERATURE)
        return ret

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            # MXValue(
            #     name='daylight',
            #     func=self.get_daylight,
            #     type=MXType.BOOL,
            #     bound=(0, 9999999),
            #     tag_list=self._default_tag_list,
            #     cycle=5,
            # ),
            MXValue(
                name='motion',
                func=self.get_motion,
                type=MXType.BOOL,
                bound=(0, 2),
                tag_list=self._default_tag_list,
                cycle=1,
            ),
            # MXValue(
            #     name='lightlevel',
            #     func=self.get_lightlevel,
            #     type=MXType.BOOL,
            #     bound=(0, 9999999),
            #     tag_list=self._default_tag_list,
            #     cycle=5,
            # ),
            # MXValue(
            #     name='temperature',
            #     func=self.get_temperature,
            #     type=MXType.BOOL,
            #     bound=(0, 9999999),
            #     tag_list=self._default_tag_list,
            #     cycle=5,
            # ),
        ]
        staff_function_list = []
        self.add_staff_service(staff_value_list + staff_function_list)
