from big_thing_py.poll_manager_thing import *
from hejhome_utils import *


class MXHejhomeStaffThing(MXStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, staff_thing_id)
        self._home_name = home_name
        self._home_id = home_id
        self._room_name = room_name
        self._room_id = room_id
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func

        self._default_tag_list: List[MXTag] = [
            MXTag(self._name),
            MXTag(self._staff_thing_id),
            # MXTag(self.home_name),
            # MXTag(self.room_name),
            MXTag('Hejhome'),
        ]
        self._default_tag_list: List[MXTag] = [
            MXTag(tag if check_valid_identifier(tag) else convert_to_valid_string(tag))
            for tag in [
                self._name,
                self._staff_thing_id,
                # self.home_name,
                # self.room_name,
                'Hejhome',
            ]
            if tag
        ]

    @MXStaffThing.print_func_info
    def get_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.STATUS)

    @override
    def make_service_list(self):
        staff_value_list = []
        staff_function_list = [
            MXFunction(
                name='state',
                func=self.get_state,
                tag_list=self._default_tag_list,
                return_type=MXType.STRING,
                arg_list=[],
                exec_time=3,
                timeout=3,
            )
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXBruntPlugHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        on_state = ret['deviceState']['power']
        return on_state

    @MXStaffThing.print_func_info
    def get_current(self):
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curCurrent'])

    @MXStaffThing.print_func_info
    def get_power(self):
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curPower']) / 10

    @MXStaffThing.print_func_info
    def get_voltage(self):
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        return float(ret['deviceState']['curVoltage']) / 10

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)

        for power, on_state in ret['deviceState'].items():
            if on_state:
                return True
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.OFF)
        if ret:
            return True
        else:
            return False

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=60
            ),
            MXValue(
                name='current',
                func=self.get_current,
                tag_list=self._default_tag_list,
                type=MXType.DOUBLE,
                bound=(0, 100000),
                cycle=60,
            ),
            MXValue(
                name='power',
                func=self.get_power,
                tag_list=self._default_tag_list,
                type=MXType.DOUBLE,
                bound=(0, 100000),
                cycle=60,
            ),
            MXValue(
                name='voltage',
                func=self.get_voltage,
                tag_list=self._default_tag_list,
                type=MXType.DOUBLE,
                bound=(0, 100000),
                cycle=60,
            ),
        ]
        staff_function_list: List[MXService] = [
            MXFunction(
                name='on',
                func=self.on,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
            ),
            MXFunction(
                name='off',
                func=self.off,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXCurtainHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_open(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)

        open_state: str = ret['deviceState']['workState']
        if open_state.lower() == 'open':
            return True
        elif open_state.lower() == 'close':
            return False

    @MXStaffThing.print_func_info
    def get_curtain_open_percent(self) -> int:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        open_percent = int(ret['deviceState']['percentState'])
        return open_percent

    @MXStaffThing.print_func_info
    def curtain_open(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.CURTAIN_OPEN)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def curtain_close(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.CURTAIN_CLOSE)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def curtain_open_control(self, percent: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self._staff_thing_id, HejHomeAction.CURTAIN_CONTROL, curtain_percent=percent
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
                name='is_open',
                func=self.is_open,
                tag_list=self._default_tag_list,
                type=MXType.BOOL,
                bound=(0, 2),
                cycle=60,
            ),
            MXValue(
                name='curtain_open_percent',
                func=self.get_curtain_open_percent,
                tag_list=self._default_tag_list,
                type=MXType.INTEGER,
                bound=(0, 100),
                cycle=60,
            ),
        ]
        staff_function_list = [
            MXFunction(
                name='curtain_open',
                func=self.curtain_open,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='curtain_close',
                func=self.curtain_close,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='curtain_open_control',
                func=self.curtain_open_control,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[MXArgument(name='curtain_open_percent', type=MXType.INTEGER, bound=(0, 100))],
                exec_time=3,
                timeout=3,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXZigbeeSwitch3HejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)

        for power, on_state in ret['deviceState'].items():
            if on_state:
                return True
        else:
            return False

    @MXStaffThing.print_func_info
    def get_sw_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        on_state = dict_to_json_string(ret['deviceState'])
        return on_state

    @MXStaffThing.print_func_info
    def on_all(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.ZBSW_ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off_all(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.ZBSW_OFF)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def set_sw(self, sw1, sw2, sw3) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self._staff_thing_id, HejHomeAction.ZBSW_CONTROL, zb_sw=(sw1, sw2, sw3)
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
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=60
            ),
            MXValue(
                name='sw_state',
                func=self.get_sw_state,
                tag_list=self._default_tag_list,
                type=MXType.STRING,
                bound=(0, 100),
                cycle=60,
            ),
        ]

        staff_function_list = [
            MXFunction(
                name='on_all',
                func=self.on_all,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='off_all',
                func=self.off_all,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='set_sw',
                func=self.set_sw,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[
                    MXArgument(name='sw1', type=MXType.BOOL, bound=(0, 2)),
                    MXArgument(name='sw2', type=MXType.BOOL, bound=(0, 2)),
                    MXArgument(name='sw3', type=MXType.BOOL, bound=(0, 2)),
                ],
                exec_time=3,
                timeout=3,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXIRDiyHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXIRAirconditionerHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.OFF)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def set_temp(self, temp: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self._staff_thing_id, HejHomeAction.SET_TEMP, temp=temp
        )
        if ret:
            return True
        else:
            return False

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = [
            MXFunction(
                name='on',
                func=self.on,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
            ),
            MXFunction(
                name='off',
                func=self.off,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
            ),
            MXFunction(
                name='set_temp',
                func=self.set_temp,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[MXArgument(name='temp', type=MXType.INTEGER, bound=(0, 100))],
            ),
        ]

        self.add_staff_service(staff_value_list + staff_function_list)


class MXLedStripRgbw2HejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        on_state = ret['deviceState']['power']
        return on_state

    @MXStaffThing.print_func_info
    def get_brightness(self) -> int:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        brightness = ret['deviceState']['brightness']
        return brightness

    @MXStaffThing.print_func_info
    def get_color(self) -> str:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, HejHomeAction.STATUS)
        color = ret['deviceState']['hsvColor']
        return dict_to_json_string(color)

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, HejHomeAction.OFF)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def set_brightness(self, brightness: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self._staff_thing_id, HejHomeAction.BRIGHTNESS, brightness=brightness
        )
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def set_color(self, r: int, g: int, b: int) -> bool:
        ret: requests.Response = self._device_function_service_func(
            self._staff_thing_id, HejHomeAction.COLOR, color=(r, g, b)
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
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=60
            ),
            MXValue(
                name='brightness',
                func=self.get_brightness,
                tag_list=self._default_tag_list,
                type=MXType.STRING,
                bound=(0, 100),
                cycle=60,
            ),
            MXValue(
                name='color',
                func=self.get_color,
                tag_list=self._default_tag_list,
                type=MXType.STRING,
                bound=(0, 100),
                cycle=60,
            ),
        ]
        staff_function_list = [
            MXFunction(
                name='on',
                func=self.on,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='off',
                func=self.off,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='set_brightness',
                func=self.set_brightness,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[MXArgument(name='brightness', type=MXType.INTEGER, bound=(0, 255))],
                exec_time=3,
                timeout=3,
            ),
            MXFunction(
                name='set_color',
                func=self.set_color,
                tag_list=self._default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[
                    MXArgument(name='r', type=MXType.INTEGER, bound=(0, 255)),
                    MXArgument(name='g', type=MXType.INTEGER, bound=(0, 255)),
                    MXArgument(name='b', type=MXType.INTEGER, bound=(0, 255)),
                ],
                exec_time=3,
                timeout=3,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXIrTvHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
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
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXRadarPIRSensorHejhomeStaffThing(MXHejhomeStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        home_name: str = '',
        home_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
        pir_status_timeout: float = 5.0,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            home_name,
            home_id,
            room_name,
            room_id,
            device_function_service_func,
            device_value_service_func,
        )
        self._pir_status: dict = {}
        self._pir_status_timeout = pir_status_timeout

    @MXStaffThing.print_func_info
    def get_pir_state(self) -> bool:
        current_time = get_current_time()
        if self._pir_status:
            if current_time - self._pir_status['t'] / 1000 > self._pir_status_timeout:
                return False
            else:
                return True
        else:
            return False

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='pir_state',
                func=self.get_pir_state,
                tag_list=self._default_tag_list,
                type=MXType.BOOL,
                bound=(0, 2),
                cycle=self._pir_status_timeout / 2,
            )
        ]
        staff_function_list = []
        self.add_staff_service(staff_value_list + staff_function_list)
