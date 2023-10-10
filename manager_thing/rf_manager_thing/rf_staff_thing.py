from big_thing_py.manager_thing import *
from queue import Queue, Empty, Full

# import struct


class MXRFStaffThing(MXStaffThing):
    def __init__(
        self,
        name: str = '',
        service_list: List[MXService] = [],
        alive_cycle: float = 10,
        device_id: str = '',
        addresses: Tuple[int, int] = (0xFFFFFFFFFFF0, 0xFFFFFFFFFFF1),
    ):
        super().__init__(name=name, service_list=service_list, alive_cycle=alive_cycle, device_id=device_id)

        self.RX_addr = addresses[0]
        self.TX_addr = addresses[1]

        # {
        #     'test_sensor_value_1': 0,
        #     'test_sensor_value_2': 0
        # }
        self.sensor_value = 0
        self.sensor_value_buffer = Queue(maxsize=int(1.2 * 60 * 10 * (1 / 0.1)))
        self.window_length = 60 * 10  # second

    def get_sensor_value(self):
        # (9, 1) [(10, 1), (11, 1), (12, 0)] (13, 0)
        # time ->
        try:
            self.sensor_value_buffer.put((time.time(), self.sensor_value), block=False)
        except Full:
            self.sensor_value_buffer.get()
            self.sensor_value_buffer.put((time.time(), self.sensor_value), block=False)
        return self.sensor_value


class MXRFStaffThingInfo(MXStaffThingInfo):
    def __init__(
        self, device_id: str, addresses: Tuple[int, int], value_name: str, value_cycle: float, alive_cycle: float
    ) -> None:
        super().__init__(device_id)
        self.addresses = addresses
        self.value_name = value_name
        self.value_cycle = value_cycle
        self.alive_cycle = alive_cycle
