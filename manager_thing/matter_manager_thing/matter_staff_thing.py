from big_thing_py.poll_manager_thing import *
from matter_utils import *

from chip.clusters.Objects import *

from matter_server.client.models.device_types import DeviceType
from matter_server.common.models import APICommand


class MXMatterStaffThing(MXStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = [],
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        node_id: int = 0,
        vendor_id: int = 0,
        product_id: int = 0,
        device_type: type[DeviceType] = None,
        send_api_command_func: Callable[[dict, float], Union[dict, bool]] = None,
    ):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, staff_thing_id)
        self._staff_thing_id = self._staff_thing_id.replace(':', '_').replace('-', '_')
        self._node_id = node_id
        self._vendor_id = vendor_id
        self._product_id = product_id
        self._device_type = device_type

        self._send_api_command: Callable[[dict, float], Union[dict, bool]] = send_api_command_func
        self._matter_server_url = f"ws://127.0.0.1:{DEFAULT_WEBSOCKET_PORT}/ws"
        self._websocket_message_id = 0

        self._default_tag_list: List[MXTag] = [
            MXTag(tag)
            for tag in [
                self._staff_thing_id,
                self._device_type.__name__,
                'Matter',
            ]
            if tag
        ]

    def get_attribute_value(self, cluster_id: int, attribute_id: int) -> str:
        result = self._send_api_command(
            command={
                'message_id': f'value_{self._websocket_message_id}',
                'command': APICommand.READ_ATTRIBUTE.value,
                'args': {
                    'node_id': self._node_id,
                    'attribute_path': f'1/{cluster_id}/{attribute_id}',
                },
            },
            timeout=10,
        )
        self._websocket_message_id += 1
        return result

    def execute_command(self, cluster_id: int, command_name: str, *args) -> str:
        payload = {arg.__name__: type(arg) for arg in args}

        result = self._send_api_command(
            command={
                'message_id': f'function_{self._websocket_message_id}',
                'command': APICommand.DEVICE_COMMAND.value,
                'args': {
                    'node_id': self._node_id,
                    'endpoint_id': 1,
                    'cluster_id': cluster_id,
                    'command_name': command_name,
                    'payload': payload,
                },
            },
            timeout=10,
        )
        self._websocket_message_id += 1
        return result

    @override
    def make_service_list(self):
        staff_value_list = []
        staff_function_list = []
        self.add_staff_service(staff_value_list + staff_function_list)


class MXOnOffLightMatterStaffThing(MXMatterStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = [],
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        node_id: int = 0,
        vendor_id: int = 0,
        product_id: int = 0,
        device_type: type[DeviceType] = None,
        send_api_command_func: Callable[[dict, float], Union[dict, bool]] = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            node_id,
            vendor_id,
            product_id,
            device_type,
            send_api_command_func,
        )

    @MXStaffThing.print_func_info
    def On(self) -> bool:
        command = OnOff.Commands.On
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def Off(self) -> bool:
        command = OnOff.Commands.Off
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def Toggle(self) -> bool:
        command = OnOff.Commands.Toggle
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def OnOff(self) -> bool:
        attribute = OnOff.Attributes.OnOff
        ret: dict = self.get_attribute_value(cluster_id=attribute.cluster_id, command_id=attribute.attribute_id)
        result = ret['result']

        return result

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                func=self.OnOff,
                type=MXType.BOOL,
                bound=(0, 2),
                tag_list=self._default_tag_list,
                cycle=5,
            ),
        ]
        staff_function_list = [
            MXFunction(
                func=self.On,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
            MXFunction(
                func=self.Off,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
            MXFunction(
                func=self.Toggle,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXDimmableLightMatterStaffThing(MXMatterStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = [],
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        node_id: int = 0,
        vendor_id: int = 0,
        product_id: int = 0,
        device_type: type[DeviceType] = None,
        send_api_command_func: Callable[[dict, float], Union[dict, bool]] = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            node_id,
            vendor_id,
            product_id,
            device_type,
            send_api_command_func,
        )

    @MXStaffThing.print_func_info
    def On(self) -> bool:
        command = OnOff.Commands.On
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def Off(self) -> bool:
        command = OnOff.Commands.Off
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def Toggle(self) -> bool:
        command = OnOff.Commands.Toggle
        ret: dict = self.execute_command(cluster_id=command.cluster_id, command_name=command.__name__)
        result = ret['result']

        return result

    @MXStaffThing.print_func_info
    def OnOff(self) -> bool:
        attribute = OnOff.Attributes.OnOff
        ret: dict = self.get_attribute_value(cluster_id=attribute.cluster_id, attribute_id=attribute.attribute_id)
        result = ret['result']

        return result

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                func=self.OnOff,
                type=MXType.BOOL,
                bound=(0, 2),
                tag_list=self._default_tag_list,
                cycle=5,
            ),
        ]
        staff_function_list = [
            MXFunction(
                func=self.On,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
            MXFunction(
                func=self.Off,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
            MXFunction(
                func=self.Toggle,
                return_type=MXType.BOOL,
                arg_list=[],
                tag_list=self._default_tag_list,
            ),
        ]
        self.add_staff_service(staff_value_list + staff_function_list)


class MXContactSensorMatterStaffThing(MXMatterStaffThing):
    def __init__(
        self,
        name: str,
        service_list: List[MXService] = [],
        alive_cycle: float = 10,
        is_super: bool = False,
        is_parallel: bool = True,
        staff_thing_id: str = '',
        node_id: int = 0,
        vendor_id: int = 0,
        product_id: int = 0,
        device_type: type[DeviceType] = None,
        send_api_command_func: Callable[[dict, float], Union[dict, bool]] = None,
    ):
        super().__init__(
            name,
            service_list,
            alive_cycle,
            is_super,
            is_parallel,
            staff_thing_id,
            node_id,
            vendor_id,
            product_id,
            device_type,
            send_api_command_func,
        )

    @MXStaffThing.print_func_info
    def StateValue(self) -> bool:
        attribute = BooleanState.Attributes.StateValue
        ret: dict = self.get_attribute_value(cluster_id=attribute.cluster_id, attribute_id=attribute.attribute_id)
        result = ret['result']

        return result

    @override
    def make_service_list(self):
        super().make_service_list()

        staff_value_list = [
            MXValue(
                name='DoorOpen',
                func=self.StateValue,
                type=MXType.BOOL,
                bound=(0, 2),
                tag_list=self._default_tag_list,
                cycle=12,
            ),
        ]
        staff_function_list = []
        self.add_staff_service(staff_value_list + staff_function_list)
