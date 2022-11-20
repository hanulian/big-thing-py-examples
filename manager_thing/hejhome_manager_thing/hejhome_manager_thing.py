from big_thing_py.manager_thing import *

from hejhome_staff_thing import *
from hejhome_utils import *
import pika


class SoPHejhomeManagerThing(SoPManagerThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 mode: SoPManagerMode = SoPManagerMode.SPLIT, network_type: SoPNetworkType = SoPNetworkType.MQTT, scan_cycle=5,
                 bridge_ip='', bridge_port=80, user_key='', conf_file_path: str = 'hejhome_room_conf.json',
                 client_id: str = '', client_secret: str = ''):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port, ssl_ca_path,
                         ssl_enable, log_name, log_enable, log_mode, append_mac_address, mode, network_type, scan_cycle)
        self._staff_thing_list: List[SoPHejhomeStaffThing] = []
        self._conf_file_path = conf_file_path

        self._bridge_ip = bridge_ip
        self._bridge_port = bridge_port
        self._user_key = user_key
        self._header = {
            "Authorization": f"Bearer {self._user_key}",
            # "Host": self.bridge_ip,
            # "Referer": "https://{host}".format(host=self.host),
            # "Accept": "*/*",
            # "Connection": "close",
            "Content-Type": "application/json;charset-UTF-8"
        }

        self._client_id = client_id
        self._client_secret = client_secret

        # Threading
        self._thread_func_list += [
            self.AMQP_listening_thread_func
        ]

    def setup(self, avahi_enable=True):
        self.load_config()

        return super().setup(avahi_enable=avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def AMQP_listening_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                credentials = pika.PlainCredentials(
                    self._client_id, self._client_secret)
                cxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ssl_options = pika.SSLOptions(
                    context=cxt, server_hostname="goqual.io")
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host='goqual.io',
                        port=55001,
                        credentials=credentials,
                        ssl_options=ssl_options
                    ))
                channel = connection.channel()

                # channel.queue_declare(queue=self._client_id)

                def callback(ch, method, properties, body):
                    # {'deviceDataReport': {'productKey': '4tljkbw8dadvdeay', 'dataId': 'AAXtA6uz9Bvw9AHL9C5YhsAfC', 'status': [{'1': 'pir', 'code': 'pir', 't': 1667974904937, 'value': 'pir'}], 'devId': '84706765c82b960c4297'}, 'deviceStatusReport': None}
                    # {'deviceDataReport': {'productKey': '4tljkbw8dadvdeay', 'dataId': 'AAXtA6u2te89AHL9C5YhsAfD', 'status': [{'1': 'none', 'code': 'pir', 't': 1667974905116, 'value': 'none'}], 'devId': '84706765c82b960c4297'}, 'deviceStatusReport': None}
                    # {'deviceDataReport': {'productKey': 'bxphqrhbh45k0hpu', 'dataId': 'AAXtA6v9BjuhjFwRnYlEDYC', 'status': [{'code': 'cur_voltage', 't': 1667974909824, 'value': 2228, '20': '2228'}], 'devId': 'ebcbfbd4976307a137qq1c'}, 'deviceStatusReport': None}

                    json_body = json.loads(body)
                    print(f" [AMQP] Received {json_body}")

                    devId = json_body['deviceDataReport']['devId']
                    # dataId = json_body['deviceDataReport']['dataId']
                    status = json_body['deviceDataReport']['status']
                    pir_status = status[0]

                    for staff_thing in self._staff_thing_list:
                        if staff_thing._device_id == devId:
                            if isinstance(staff_thing, SoPRadarPIRSensorHejhomeStaffThing):
                                if pir_status['value'] == 'pir':
                                    staff_thing._pir_status = pir_status
                                    break

                channel.basic_consume(queue=self._client_id,
                                      on_message_callback=callback, auto_ack=True)

                print(' [*] Waiting for messages. To exit press CTRL+C')
                channel.start_consuming()

                if msg is None:
                    # print('msg is None...')
                    continue
                else:
                    self._staff_receive_queue.put(msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

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

    def _handle_staff_message(self, msg: str):
        protocol_type = None
        hejhome_device_list: Dict = msg

        try:
            if hejhome_device_list == False:
                protocol_type = [SoPProtocolType.Base.TM_ALIVE]
            elif 'result' in hejhome_device_list:
                protocol_type = [
                    SoPProtocolType.Base.TM_REGISTER, SoPProtocolType.Base.TM_ALIVE]
        except Exception as e:
            SOPLOG_DEBUG(
                f'[_handle_staff_message] Failed to get hejhome_device_list...', 'red')
            protocol_type = []

        if SoPProtocolType.Base.TM_REGISTER in protocol_type:
            self._handle_staff_REGISTER(msg)
        elif SoPProtocolType.Base.TM_ALIVE in protocol_type:
            self._handle_staff_ALIVE(msg)
        elif SoPProtocolType.Base.TM_VALUE_PUBLISH in protocol_type or SoPProtocolType.Base.TM_VALUE_PUBLISH_OLD in protocol_type:
            self._handle_staff_VALUE_PUBLISH(msg)
        elif SoPProtocolType.Base.TM_RESULT_EXECUTE in protocol_type:
            self._handle_staff_RESULT_EXECUTE(msg)

    def _send_staff_message(self, msg: Union[StaffRegisterResult, None]):
        if type(msg) == StaffRegisterResult:
            self._send_staff_RESULT_REGISTER(msg)
        elif type(msg) == None:
            pass
        else:
            self._publish_staff_packet(msg)

    def _handle_staff_REGISTER(self, msg):
        try:
            hejhome_home_list = msg
            hejhome_device_info = {'home_list': []}
            for home in hejhome_home_list['result']:
                room_list = API_request(
                    url='%s/homes/%s/rooms' % (self._bridge_ip, home['homeId']), header=self._header, body='')
                if not room_list:
                    return False
                room_list['home_id'] = home['homeId']
                hejhome_device_info['home_list'].append(room_list)

            for home in hejhome_device_info['home_list']:
                home_id = home['home_id']

                for room in home['rooms']:
                    room_id = room['room_id']
                    device_list = API_request(
                        url=f'{self._bridge_ip}/homes/{home_id}/rooms/{room_id}/devices', header=self._header, body='', method=RequestMethod.GET)
                    if device_list:
                        for device in device_list:
                            device['roomId'] = room_id
                            device['homeId'] = home_id
                        room['device_list'] = device_list
                    else:
                        room['device_list'] = []

            for home in hejhome_device_info['home_list']:
                room_list = home['rooms']
                for room in room_list:
                    device_list = room['device_list']
                    for device in device_list:
                        staff_thing_info = SoPHejhomeStaffThingInfo(
                            device_id=device['id'], hejhome_info=device)
                        self._staff_register_queue.put(staff_thing_info)
        except Exception as e:
            print_error(e)

    def _handle_staff_ALIVE(self, msg):
        hejhome_device_list = msg
        pass

    def _handle_staff_VALUE_PUBLISH(self, msg):
        hejhome_device_list = msg
        pass

    def _handle_staff_RESULT_EXECUTE(self, msg):
        hejhome_device_list = msg
        pass

    def _send_staff_RESULT_REGISTER(self, register_result: StaffRegisterResult):
        if register_result.device_id is None:
            raise ValueError('staff thing device_id is None')

        SOPLOG_DEBUG(
            f'[_send_staff_RESULT_REGISTER] Register {register_result.staff_thing_name} complete!!!')

    def _send_staff_EXECUTE(self, msg):
        pass

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    # override
    def _receive_staff_packet(self):
        cur_time = time.time()

        # for discover hejhome staff thing
        staff_api_fail = False
        for staff_thing in self._staff_thing_list:
            if staff_thing._api_fail:
                staff_api_fail = True

        if cur_time - self._last_scan_time > self._scan_cycle or staff_api_fail:
            if staff_api_fail:
                SOPLOG_DEBUG(
                    'Staff things list update... (StaffThing\'s API request failed)', 'yellow')
            else:
                SOPLOG_DEBUG('Staff things list update...', 'blue')

            hejhome_home_list = API_request(
                url=f'{self._bridge_ip}/homes', header=self._header, body='')

            for staff_thing in self._staff_thing_list:
                self._send_TM_ALIVE(staff_thing.get_name())
                staff_thing.set_last_alive_time(cur_time)
            if self.verify_hejhome_request_result(hejhome_home_list):
                self._last_scan_time = cur_time
                return hejhome_home_list
            else:
                return False
        else:
            for staff_thing in self._staff_thing_list:
                # for check hejhome staff thing alive
                if staff_thing.get_registered() and cur_time - staff_thing.get_last_alive_time() > staff_thing.get_alive_cycle():
                    hejhome_home_list = API_request(
                        url=f'{self._bridge_ip}/homes/{staff_thing._home_id}/rooms/{staff_thing._room_id}', header=self._header, body='')
                    if self.verify_hejhome_request_result(hejhome_home_list):
                        self._send_TM_ALIVE(staff_thing.get_name())
                        staff_thing.set_last_alive_time(cur_time)
                        return hejhome_home_list
                    else:
                        return False
                # for check hejhome staff thing value publish cycle
                else:
                    for value in staff_thing.get_value_list():
                        if cur_time - value.get_last_update_time() > value.get_cycle():
                            # update() method update _last_update_time of SoPValue
                            value.update()
                            self._send_TM_VALUE_PUBLISH(
                                value.get_name(), value.dump_pub())

        return None

    # override
    def _publish_staff_packet(self, msg):
        pass

    def load_config(self):
        conf_file = json_file_read(self._conf_file_path)

        # FIXME: Thig code have some issue when conf file was not exist.... Fix it
        if conf_file:
            account_name = conf_file['select']
            hejhome_account_info = conf_file['account_list']
            for account in hejhome_account_info:
                if account_name == account['account_name']:
                    self._bridge_ip = account['bridge_ip'].strip('/')
                    self._bridge_port = int(account['bridge_port'])
                    self._user_key = account['user_key']
        elif self._bridge_ip == '' or self._bridge_ip == None:
            SOPLOG_DEBUG('bridge ip is empty. exit program...', 'red')
            raise Exception('HueConfigFileNotExist')

    def verify_hejhome_request_result(self, result_list: list):
        if type(result_list) == list and 'error' in result_list[0]:
            print_error(result_list[0]['error']['description'])
            return False
        else:
            return True

    # override
    def _create_staff(self, staff_thing_info: SoPHejhomeStaffThingInfo) -> SoPHejhomeStaffThing:
        staff_info = staff_thing_info.hejhome_info

        uniqueid = staff_info['id']
        name = staff_info['name'].replace(' ', '_')
        home_name = None
        deviceType = staff_info['deviceType']
        hasSubDevices = staff_info['hasSubDevices']
        modelName = staff_info['modelName']
        # int(family_id) == home_id
        family_id = staff_info['familyId']
        home_id = staff_info['homeId']
        room_id = staff_info['roomId']
        category = staff_info['category']
        online = staff_info['online']
        locate = name.split('__')[-1]
        name = name.split('__')[0]

        tag_list = [SoPTag(uniqueid),
                    SoPTag(deviceType),
                    SoPTag(name),
                    SoPTag(locate)]

        hejhome_child_thing = SoPHejhomeStaffThing(
            name=name, service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)

        if deviceType == 'BruntPlug':
            hejhome_child_thing = SoPBruntPlugHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)
            staff_function_list: List[SoPFunction] = []
            staff_value_list: List[SoPValue] = []
            staff_service_list: List[SoPService] = staff_value_list + \
                staff_function_list

            for staff_service in staff_service_list:
                for tag in tag_list:
                    staff_service.add_tag(tag)

                hejhome_child_thing._add_service(staff_service)
        elif deviceType == 'Curtain':
            hejhome_child_thing = SoPCurtainHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)

            # curtain_open
            curtain_open_function = SoPFunction(
                name='curtain_open', func=hejhome_child_thing.curtain_open,
                return_type=type_converter(get_function_return_type(hejhome_child_thing.curtain_open)), arg_list=[])

            # curtain_close
            curtain_close_function = SoPFunction(
                name='curtain_close', func=hejhome_child_thing.curtain_close,
                return_type=type_converter(get_function_return_type(hejhome_child_thing.curtain_close)), arg_list=[])

            staff_function_list: List[SoPFunction] = [curtain_open_function,
                                                      curtain_close_function]
            staff_value_list: List[SoPValue] = []
            staff_service_list: List[SoPService] = staff_value_list + \
                staff_function_list

            for staff_service in staff_service_list:
                for tag in tag_list:
                    staff_service.add_tag(tag)

                hejhome_child_thing._add_service(staff_service)
        elif deviceType == 'ZigbeeSwitch3':
            hejhome_child_thing = SoPZigbeeSwitch3HejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)

            arg_on = SoPArgument(
                name='on', type=SoPType.BOOL, bound=(0, 2))
            # switch1_set
            switch1_set_function = SoPFunction(
                name='switch1_set', func=hejhome_child_thing.switch1_set,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.switch1_set)),
                arg_list=[arg_on, ])

            # switch2_set
            switch2_set_function = SoPFunction(
                name='switch2_set', func=hejhome_child_thing.switch2_set,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.switch2_set)),
                arg_list=[arg_on, ])

            # switch3_set
            switch3_set_function = SoPFunction(
                name='switch3_set', func=hejhome_child_thing.switch3_set,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.switch3_set)),
                arg_list=[arg_on, ])

            # all_switch_set
            all_switch_set_function = SoPFunction(
                name='all_switch_set', func=hejhome_child_thing.all_switch_set,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.all_switch_set)),
                arg_list=[arg_on, ])

            staff_function_list: List[SoPFunction] = [switch1_set_function,
                                                      switch2_set_function,
                                                      switch3_set_function,
                                                      all_switch_set_function]
            staff_value_list: List[SoPValue] = []
            staff_service_list: List[SoPService] = staff_value_list + \
                staff_function_list

            for staff_service in staff_service_list:
                for tag in tag_list:
                    staff_service.add_tag(tag)

                hejhome_child_thing._add_service(staff_service)
        elif deviceType == 'IrDiy':
            hejhome_child_thing = SoPIrDiyHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)
        elif deviceType == 'IrAirconditioner':
            hejhome_child_thing = SoPIrAirconditionerHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)
        elif deviceType == 'LedStripRgbw2':
            hejhome_child_thing = SoPLedStripRgbw2HejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)

            # set_brightness
            arg_brightness = SoPArgument(
                name='brightness', type=SoPType.INTEGER, bound=(0, 255))
            set_brightness_function = SoPFunction(
                name='set_brightness', func=hejhome_child_thing.set_brightness,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.set_brightness)),
                arg_list=[arg_brightness])

            # set_color
            arg_r = SoPArgument(
                name='r', type=SoPType.INTEGER, bound=(0, 255))
            arg_g = SoPArgument(
                name='g', type=SoPType.INTEGER, bound=(0, 255))
            arg_b = SoPArgument(
                name='b', type=SoPType.INTEGER, bound=(0, 255))
            set_color_function = SoPFunction(
                name='set_color', func=hejhome_child_thing.set_color,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.set_color)),
                arg_list=[arg_r, arg_g, arg_b])

            staff_function_list: List[SoPFunction] = [set_brightness_function,
                                                      set_color_function]
            staff_value_list: List[SoPValue] = []
            staff_service_list: List[SoPService] = staff_value_list + \
                staff_function_list

            for staff_service in staff_service_list:
                for tag in tag_list:
                    staff_service.add_tag(tag)

                hejhome_child_thing._add_service(staff_service)
        elif deviceType == 'IrTv':
            hejhome_child_thing = SoPIrTvHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)
        elif deviceType == 'SensorRadar':
            hejhome_child_thing = SoPRadarPIRSensorHejhomeStaffThing(
                name=f'{deviceType}_{uniqueid}', service_list=[], alive_cycle=60 * 60, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, home_id=home_id, room_id=room_id, device_id=uniqueid)
            get_pir_status_func = SoPFunction(
                name='get_pir_status', func=hejhome_child_thing.get_pir_status,
                return_type=type_converter(
                    get_function_return_type(hejhome_child_thing.get_pir_status)),
                arg_list=[])

            staff_function_list: List[SoPFunction] = [get_pir_status_func]
            staff_value_list: List[SoPValue] = []
            staff_service_list: List[SoPService] = staff_value_list + \
                staff_function_list

            for staff_service in staff_service_list:
                for tag in tag_list:
                    staff_service.add_tag(tag)

                hejhome_child_thing._add_service(staff_service)
        else:
            SOPLOG_DEBUG('Unexpected function!!!', 'red')

        # on
        on_function = SoPFunction(
            name='on', func=hejhome_child_thing.on,
            return_type=type_converter(get_function_return_type(hejhome_child_thing.on)), arg_list=[])

        # off
        off_function = SoPFunction(
            name='off', func=hejhome_child_thing.off,
            return_type=type_converter(get_function_return_type(hejhome_child_thing.off)), arg_list=[])

        staff_function_list: List[SoPFunction] = [on_function,
                                                  off_function]
        staff_value_list: List[SoPValue] = []
        staff_service_list: List[SoPService] = staff_value_list + \
            staff_function_list

        for staff_service in staff_service_list:
            for tag in tag_list:
                staff_service.add_tag(tag)

            hejhome_child_thing._add_service(staff_service)

        return hejhome_child_thing
