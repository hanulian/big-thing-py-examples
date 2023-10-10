from big_thing_py.manager_thing import *
from rf_staff_thing import *

# import struct
import time

try:
    from RF24 import RF24, RF24_PA_LOW, RF24_PA_MAX
except ImportError:
    MXLOG_DEBUG('RF24 not found')


class MXRFManagerThing(MXManagerThing):
    RF_MANAGER_TIMEOUT = 0.00001

    def __init__(
        self,
        name: str = None,
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        is_super: bool = False,
        is_parallel: bool = True,
        ip: str = None,
        port: int = None,
        ssl_ca_path: str = None,
        ssl_enable: bool = None,
        mode: MXManagerMode = MXManagerMode.SPLIT,
        network_type: MXNetworkType = MXNetworkType.RF,
        scan_cycle: int = 10,
        rf_pin: Tuple[int, int] = (22, 0),
        addresses: Tuple[int, int] = (0xFFFFFFFFFFF0, 0xFFFFFFFFFFF1),
        power_mode: MXRFPowerMode = MXRFPowerMode.HIGH,
    ):
        super().__init__(
            name=name,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=is_super,
            is_parallel=is_parallel,
            ip=ip,
            port=port,
            ssl_ca_path=ssl_ca_path,
            ssl_enable=ssl_enable,
            manager_mode=mode,
            network_type=network_type,
            scan_cycle=scan_cycle,
        )

        self._radio: RF24 = RF24(*rf_pin)
        # self._radio: RF24 = RF24(22, 0)
        self._TX_address = addresses[0]
        self._RX_address = addresses[1]
        self._power_mode = power_mode

        self._staff_thing_list: List[MXRFStaffThing] = []

    @override
    def setup(self, avahi_enable=True):
        self._RF_init()

        tag = [
            MXTag('RFManagerThing'),
        ]

        activated_sensor_num_value = MXValue(
            name='activated_sensor_num_value',
            tag_list=tag,
            desc='',
            func=self.get_activate_sensor_num,
            type=MXType.INTEGER,
            bound=(0, 2000),
            format='',
            cycle=1,
        )
        sensor_avg_value = MXValue(
            name='sensor_avg_value',
            tag_list=tag,
            desc='',
            func=self.sensor_avg,
            type=MXType.INTEGER,
            bound=(0, 2000),
            format='',
            cycle=1,
        )
        sensor_MAX_value = MXValue(
            name='sensor_MAX_value',
            tag_list=tag,
            desc='',
            func=self.sensor_MAX,
            type=MXType.INTEGER,
            bound=(0, 2000),
            format='',
            cycle=1,
        )
        sensor_min_value = MXValue(
            name='sensor_min_value',
            tag_list=tag,
            desc='',
            func=self.sensor_min,
            type=MXType.INTEGER,
            bound=(0, 2000),
            format='',
            cycle=1,
        )

        get_sensor_value_func = MXFunction(
            name='get_sensor_value_func',
            tag_list=tag,
            desc='',
            func=self.get_sensor_value,
            return_type=MXType.INTEGER,
            exec_time=3,
            timeout=3,
        )
        sensor_avg_func = MXFunction(
            name='sensor_avg_func',
            tag_list=tag,
            desc='',
            func=self.sensor_avg,
            return_type=MXType.INTEGER,
            exec_time=3,
            timeout=3,
        )
        sensor_MAX_func = MXFunction(
            name='sensor_MAX_func',
            tag_list=tag,
            desc='',
            func=self.sensor_MAX,
            return_type=MXType.INTEGER,
            exec_time=3,
            timeout=3,
        )
        sensor_min_func = MXFunction(
            name='sensor_min_func',
            tag_list=tag,
            desc='',
            func=self.sensor_min,
            return_type=MXType.INTEGER,
            exec_time=3,
            timeout=3,
        )
        self.add_service(activated_sensor_num_value)
        self.add_service(sensor_avg_value)
        self.add_service(sensor_MAX_value)
        self.add_service(sensor_min_value)

        self.add_service(get_sensor_value_func)
        self.add_service(sensor_avg_func)
        self.add_service(sensor_MAX_func)
        self.add_service(sensor_min_func)

        super().setup(avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    # nothing to add...

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    # nothing to add...

    # ==================================================================================================================================
    #  _   _                    _  _                     _                   _                           _
    # | | | |                  | || |                   | |                 | |                         | |
    # | |_| |  __ _  _ __    __| || |  ___   ___  _   _ | |__   _ __    ___ | |_ __      __  ___   _ __ | | __  _ __ ___   ___   __ _
    # |  _  | / _` || '_ \  / _` || | / _ \ / __|| | | || '_ \ | '_ \  / _ \| __|\ \ /\ / / / _ \ | '__|| |/ / | '_ ` _ \ / __| / _` |
    # | | | || (_| || | | || (_| || ||  __/ \__ \| |_| || |_) || | | ||  __/| |_  \ V  V / | (_) || |   |   <  | | | | | |\__ \| (_| |
    # \_| |_/ \__,_||_| |_| \__,_||_| \___| |___/ \__,_||_.__/ |_| |_| \___| \__|  \_/\_/   \___/ |_|   |_|\_\ |_| |_| |_||___/ \__, |
    #                                                                                                                            __/ |
    #                                                                                                                           |___/
    # ==================================================================================================================================

    def _handle_staff_message(self, msg: bytearray):
        try:
            protocol_type: MXRFProtocol = MXRFProtocol(msg[:4].rstrip().rstrip(b'\x00').decode())
        except ValueError as e:
            MXLOG_DEBUG(f'[_handle_staff_message] MXRFProtocol type error : {msg}')
            print_error(e)
            return False
        except Exception as e:
            MXLOG_DEBUG(f'[_handle_staff_message]: some error but not ValueError')
            print_error(e)
            return False

        if protocol_type == MXRFProtocol.REG:
            self._handle_staff_REGISTER(msg)
        elif protocol_type == MXRFProtocol.LIVE:
            self._handle_staff_ALIVE(msg)
        elif protocol_type == MXRFProtocol.VAL:
            self._handle_staff_VALUE_PUBLISH(msg)
        elif protocol_type == MXRFProtocol.EACK:
            self._handle_staff_RESULT_EXECUTE(msg)

    # TODO: implement this
    def _send_staff_message(self, msg: Union[StaffRegisterResult, None]):
        if type(msg) == StaffRegisterResult:
            self._send_staff_RESULT_REGISTER(msg)
        elif type(msg) == None:
            pass
        else:
            self._publish_staff_message(msg)

    def _handle_staff_REGISTER(self, msg: bytearray = None):
        rf_msg = decode_RF_message(msg)

        try:
            if rf_msg:
                MXLOG_DEBUG(f'[_handle_staff_REGISTER]: Receive REG message from {rf_msg.device_id} device', 'green')

                # time.sleep(0.1)
                # staff_thing_id = hex(random.randint(0, 0xFFFF))[2:].upper()
                value_name = rf_msg.service_name
                if 'A' in rf_msg.payload or 'V' in rf_msg.payload:
                    alive_cycle = int(rf_msg.payload.split('A')[1].split('V')[0]) / 1000
                    value_cycle = int(rf_msg.payload.split('A')[1].split('V')[1].strip()) / 1000
                else:
                    MXLOG_DEBUG(f'Alive cycle or value cycle is not found... {msg}', 'red')
                    return False

                staff_info = MXRFStaffThingInfo(
                    device_id=rf_msg.device_id,
                    addresses=(self._TX_address, self._RX_address),
                    value_name=value_name,
                    value_cycle=value_cycle,
                    alive_cycle=alive_cycle,
                )

                self._staff_register_queue.put(staff_info)
            else:
                MXLOG_DEBUG(f'[_handle_staff_REGISTER] decode_RF_message error!!!')
        except Exception as e:
            MXLOG_DEBUG(f'[_handle_staff_REGISTER]: {rf_msg.device_id} device register error : {e}')
            print_error(e)
            return False

    def _handle_staff_ALIVE(self, msg: bytearray = None):
        try:
            device_id = msg[4:7].decode()
            payload = msg[8:].decode()

            for staff_thing in self._staff_thing_list:
                if f'RF_{device_id}' == staff_thing.get_name():
                    alive_info = {'staff_thing_name': staff_thing.get_name(), 'alive_recv_time': get_current_time()}
                    self._staff_alive_queue.put(alive_info)
        except Exception as e:
            MXLOG_DEBUG(f'[_handle_staff_ALIVE]: some error : {e}')
            print_error(e)
            return False

    def _handle_staff_VALUE_PUBLISH(self, msg: bytearray = None):
        rf_msg = decode_RF_message(msg)

        try:
            if rf_msg:
                for staff_thing in self._staff_thing_list:
                    if f'RF_{rf_msg.device_id}' == staff_thing.get_name():
                        MXLOG_DEBUG(
                            f'[_handle_staff_VALUE_PUBLISH]: Receive VAL message from {rf_msg.device_id} device. payload : {rf_msg.payload}',
                            'green',
                        )
                        for value in staff_thing.get_value_list():
                            if rf_msg.service_name == value.get_name():
                                value_type = value.get_type()
                                # value.set_arg_list([rf_msg.service_name, ])
                                MXLOG_DEBUG(
                                    f'[_handle_staff_VALUE_PUBLISH]: Update {rf_msg.device_id} device {rf_msg.service_name} value to {rf_msg.payload}',
                                    'green',
                                )
                                try:
                                    if value_type == MXType.INTEGER:
                                        staff_thing.sensor_value = int(rf_msg.payload)
                                    elif value_type == MXType.DOUBLE:
                                        staff_thing.sensor_value = float(rf_msg.payload)
                                    elif value_type in [MXType.STRING, MXType.BINARY]:
                                        staff_thing.sensor_value = str(rf_msg.payload)
                                    elif value_type == MXType.BOOL:
                                        staff_thing.sensor_value = bool(rf_msg.payload)
                                    else:
                                        raise ValueError('[_handle_staff_VALUE_PUBLISH] Unknown value type')
                                except Exception as e:
                                    MXLOG_DEBUG(
                                        f'[_handle_staff_VALUE_PUBLISH]: {rf_msg.device_id} device {rf_msg.service_name} value error... it may be overflow : {e}'
                                    )
                                    print_error(e)
                                    return False

                            value.update()

                            return True
                else:
                    MXLOG_DEBUG(
                        f'[_handle_staff_VALUE_PUBLISH]: Not registered device message... : {rf_msg.device_id}',
                        'yellow',
                    )
            else:
                MXLOG_DEBUG(f'[_handle_staff_VALUE_PUBLISH] \'rf_msg\' get cracked... skip value update...')
        except Exception as e:
            MXLOG_DEBUG(f'[_handle_staff_VALUE_PUBLISH] error : {e}')
            print_error(e)
            return False

    # TODO: implement this
    def _handle_staff_RESULT_EXECUTE(self, msg: bytearray = None):
        pass

    def _send_staff_RESULT_REGISTER(self, register_result: StaffRegisterResult):
        if register_result.device_id is None:
            raise ValueError('staff thing device_id is None')

        publish_buffer = bytearray(
            f'RACK{register_result.device_id}{register_result.assigned_device_id}'.encode('utf-8')
        )

        MXLOG_DEBUG(
            f'[_handle_staff_RESULT_EXECUTE] Send REGACK. staff id : {register_result.device_id} - {register_result.assigned_device_id}'
        )
        self._staff_publish_queue.put(publish_buffer)

    # TODO: implement this
    def _send_staff_EXECUTE(self):
        pass

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _RF_init(self):
        # [0xFFFFFFFFFFF0, 0xFFFFFFFFFFF1
        if not self._radio.begin():
            raise RuntimeError("radio hardware is not responding")

        self._radio.powerDown()
        time.sleep(1)
        self._radio.powerUp()

        if self._power_mode == MXRFPowerMode.HIGH:
            self._radio.setPALevel(RF24_PA_MAX)
        elif self._power_mode == MXRFPowerMode.LOW:
            self._radio.setPALevel(RF24_PA_LOW)
        else:
            raise ValueError('Invalid power mode')
        self._radio.enableDynamicPayloads()
        self._radio.enableAckPayload()
        # self._radio.setChannel(76)

        self._radio.openWritingPipe(self._TX_address)
        self._radio.openReadingPipe(1, self._RX_address)

        self._radio.startListening()
        self._radio.printPrettyDetails()

    def _create_staff(self, staff_info: MXRFStaffThingInfo) -> MXRFStaffThing:
        staff_thing_id = staff_info.device_id
        TX_address = staff_info.addresses[0]
        RX_address = staff_info.addresses[1]

        value_name = staff_info.value_name
        alive_cycle = staff_info.alive_cycle
        value_cycle = staff_info.value_cycle

        staff_thing = MXRFStaffThing(
            name=f'RF_{staff_thing_id}',
            alive_cycle=alive_cycle,
            addresses=(TX_address, RX_address),
            device_id=staff_thing_id,
        )

        test_sensor_value = MXValue(
            name=value_name,
            tag_list=[],
            desc='',
            func=staff_thing.get_sensor_value,
            type=MXType.INTEGER,
            bound=(0, 1000),
            format='',
            cycle=value_cycle,
        )
        staff_thing._add_value(test_sensor_value)

        return staff_thing

    def _receive_staff_message(self) -> Union[bytearray, None]:
        # radio.startListening()

        start_timer = time.time()
        while (time.time() - start_timer) < 5:
            has_payload, pipe_num = self._radio.available_pipe()
            if has_payload:
                length = self._radio.getDynamicPayloadSize()
                received_packet = self._radio.read(length)
                print(f"Received {length} bytes on pipe {pipe_num}: {received_packet}")
                return received_packet
        else:
            # no paylcdcdoad received
            return None

    def _publish_staff_message(self, msg: bytearray) -> None:
        self._radio.stopListening()
        cnt = 3
        while cnt:
            self._radio.write(msg)
            time.sleep(0.1)
            cnt -= 1
        self._radio.startListening()

    # Manager Things' function service ========================

    def get_sensor_value(self, device_id: str) -> int:
        cur_time = time.time()
        for sensor in self._staff_thing_list:
            if device_id == sensor.get_device_id():
                Sum = 0
                for sensor_time, value in reversed(sensor.sensor_value_buffer.queue):
                    if cur_time - sensor_time < sensor.window_length:
                        Sum += value
                return 1 if int(Sum) >= 1 else 0

    def get_activate_sensor_num(self) -> int:
        sensor_value_list = []

        for sensor in self._staff_thing_list:
            sensor_value_list.append(self.get_sensor_value(sensor.get_device_id()))

        return sensor_value_list.count(1)

    def sensor_avg(self) -> int:
        sensor_value_list = []

        for sensor in self._staff_thing_list:
            sensor_value_list.append(self.get_sensor_value(sensor.get_device_id()))

        Sum = sum(sensor_value_list)
        Len = len(sensor_value_list)
        result = round(sum(sensor_value_list) / len(sensor_value_list) if len(sensor_value_list) != 0 else 0)
        print(f'movement average : {result}')
        return result

    def sensor_MAX(self) -> int:
        sensor_value_list = []

        for sensor in self._staff_thing_list:
            sensor_value_list.append(self.get_sensor_value(sensor.get_device_id()))

        result = max(sensor_value_list) if len(sensor_value_list) != 0 else 0
        print(f'movement max : {result}')
        return result

    def sensor_min(self) -> int:
        sensor_value_list = []

        for sensor in self._staff_thing_list:
            sensor_value_list.append(self.get_sensor_value(sensor.get_device_id()))

        result = min(sensor_value_list) if len(sensor_value_list) != 0 else 0
        print(f'movement min : {result}')
        return result
