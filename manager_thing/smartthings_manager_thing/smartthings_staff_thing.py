from big_thing_py.poll_manager_thing import *
from smartthings_utils import *
from big_thing_py.utils.json_util import *


class MXSmartThingsStaffThing(MXStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
        device_function_service_func: Callable = None,
        device_value_service_func: Callable = None,
    ):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, staff_thing_id)

        self._label = label
        self._location_name = location_name
        self._room_name = room_name
        self._location_id = location_id
        self._room_id = room_id
        self._device_type = device_type
        self._device_function_service_func = device_function_service_func
        self._device_value_service_func = device_value_service_func

        self._default_tag_list: List[MXTag] = [
            MXTag(tag if check_valid_identifier(tag) else convert_to_valid_string(tag))
            for tag in [
                # self._name,
                self._staff_thing_id,
                self._location_name,
                self._location_id,
                self._room_name,
                self._room_id,
                self._device_type,
                self._label,
                'SmartThings',
            ]
            if tag
        ]

    @MXStaffThing.print_func_info
    def get_state(self) -> str:
        ret: requests.Response = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.STATUS)

        if ret:
            return dict_to_json_string(ret)
        else:
            MXLOG_DEBUG(f'fail to get state of Smartthings device...', 'red')
            raise

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
            )
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXAirPurifierSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, SmartThingsAction.STATUS)
        if ret:
            on_state = ret['components']['main']['switch']['switch']['value']
            if on_state == 'on':
                return True
            elif on_state == 'off':
                return False
            else:
                MXLOG_DEBUG(f'unexpected device state: {on_state}', 'red')
                return False
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.OFF)
        if ret:
            return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=20
            )
        ]
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
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXBluetoothTrackerSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXChargerSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXHubSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXLightSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXRobotCleanerSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, SmartThingsAction.STATUS)
        if ret:
            on_state = ret['components']['main']['switch']['switch']['value']
            if on_state == 'on':
                return True
            elif on_state == 'off':
                return False
            else:
                MXLOG_DEBUG(f'unexpected device state: {on_state}', 'red')
                return False
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.OFF)
        if ret:
            return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=20
            )
        ]
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
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXSmartLockSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = []
        staff_function_list = []

        self.add_staff_service(staff_value_list + staff_function_list)


class MXSmartPlugSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, SmartThingsAction.STATUS)
        if ret:
            on_state = ret['components']['main']['switch']['switch']['value']
            if on_state == 'on':
                return True
            elif on_state == 'off':
                return False
            else:
                MXLOG_DEBUG(f'unexpected device state: {on_state}', 'red')
                return False
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.OFF)
        if ret:
            return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=20
            )
        ]
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
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXSwitchSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, SmartThingsAction.STATUS)
        if ret:
            on_state = ret['components']['main']['switch']['switch']['value']
            if on_state == 'on':
                return True
            elif on_state == 'off':
                return False
            else:
                MXLOG_DEBUG(f'unexpected device state: {on_state}', 'red')
                return False
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.OFF)
        if ret:
            return True
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=20
            )
        ]
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
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXTelevisionSmartThingsStaffThing(MXSmartThingsStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = None,
        label: str = '',
        location_name: str = '',
        location_id: str = '',
        room_name: str = '',
        room_id: str = '',
        device_type: str = '',
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
            label,
            location_name,
            location_id,
            room_name,
            room_id,
            device_type,
            device_function_service_func,
            device_value_service_func,
        )

    @MXStaffThing.print_func_info
    def is_on(self) -> bool:
        ret: requests.Response = self._device_value_service_func(self._staff_thing_id, SmartThingsAction.STATUS)
        if ret:
            on_state = ret['components']['main']['switch']['switch']['value']
            if on_state == 'on':
                return True
            elif on_state == 'off':
                return False
            else:
                MXLOG_DEBUG(f'unexpected device state: {on_state}', 'red')
                return False
        else:
            return False

    @MXStaffThing.print_func_info
    def on(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.ON)
        if ret:
            return True
        else:
            return False

    @MXStaffThing.print_func_info
    def off(self) -> bool:
        ret = self._device_function_service_func(self._staff_thing_id, SmartThingsAction.OFF)
        if ret:
            return ret
        else:
            return False

    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='is_on', func=self.is_on, tag_list=self._default_tag_list, type=MXType.BOOL, bound=(0, 2), cycle=20
            )
        ]
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
        ]
        self.add_staff_service(staff_value_list + staff_function_list)
