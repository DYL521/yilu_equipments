from external_api.base import ExternalAPIBase
# from PyCRC.CRCCCITT import CRCCCITT
from external_api.const import SamsungAirConditionerDirection, SamsungAirConditionerSpeed, SamsungAirConditionerMode
import requests
import json

class SamsungAirConditioner(ExternalAPIBase):
    MANUFACTURE = "samsung_air_conditioner"

    def provide_airconditioner_change_mode(self, device_id, **kwargs):
        '''request_data注解
        indoor_unit_address : 室内机地址, 一台室外机可以绑定四十八台室内机, 00~3F
        outdoor_unit_address : 室外机地址, 当有多台室内机时, 由此地址区分 D0~DF
        wind_direction : 风向，  1A : 上/下  1B : 左/右  1C : 全部方向  1F : 停止
        temperature_and_wind_speed : 设定温度Bit 43210  10000 : 16'C ~  11110 : 30'C
                                         风速Bit 765   000 : Auto   010 : Low   100 : Mid   101 : Hig
        is_on : 室内机开关， F4H : 开  C4H : 关
        checksum : crc16_ccitt校验过的结果
        '''
        indoor_unit_address = device_id[:2]
        outdoor_unit_address = hex(int(device_id[2:]))[2:].upper().zfill(2)

        wd_decimalism = kwargs['wind_direction'] == 'not sure' and \
                        list(SamsungAirConditionerDirection.values.keys())[
            list(SamsungAirConditionerDirection.values.values()).index('stop')] or \
                        list(SamsungAirConditionerDirection.values.keys())[
            list(SamsungAirConditionerDirection.values.values()).index(kwargs['wind_direction'].replace('_', ' '))]

        wind_direction = hex(wd_decimalism)[2:].upper()

        if kwargs['wind_speed'] == 'not sure':
            ws_decimalism = list(SamsungAirConditionerSpeed.values.keys())[
            list(SamsungAirConditionerSpeed.values.values()).index('auto')]
        else:
            ws_decimalism = list(SamsungAirConditionerSpeed.values.keys())[
                list(SamsungAirConditionerSpeed.values.values()).index(kwargs['wind_speed'].replace('_', ' '))]

        temperature_and_wind_speed = hex(int(str(bin(ws_decimalism)[2:].zfill(3)) +
                                             str(bin(kwargs['temperature'])[2:]),2))[2:].upper().zfill(2)

        if kwargs['mode'] == 'not sure':
            mode_decimalism = list(SamsungAirConditionerMode.values.keys())[
                list(SamsungAirConditionerMode.values.values()).index('auto')]
        else:
            mode_decimalism = list(SamsungAirConditionerMode.values.keys())[
                list(SamsungAirConditionerMode.values.values()).index(kwargs['mode'].replace('_', ' '))]

        mode = hex(mode_decimalism)[2:].upper().zfill(2)

        is_on = (kwargs['is_on']) == True and 'F4' or 'C4'
        checksum = self.crc16_ccitt(
            f'F0 {indoor_unit_address} B0 00 01 {outdoor_unit_address} {wind_direction} 00 '
            f'{temperature_and_wind_speed} {mode} {is_on}')

        request_data = f'32 F0 {indoor_unit_address} B0 00 01 {outdoor_unit_address} {wind_direction} 00 ' \
                       f'{temperature_and_wind_speed} {mode} {is_on} {checksum} 00 0F 34'
        samsung_data = self.samsung_requsets(request_data, kwargs['url'])
        return samsung_data

    def provide_airconditioner_query(self, device_id, **kwargs):
        '''
        温度  室温        送风的方向和速度      模式/
         4D    51   6463         FE              80    40F30050
        :param device_id: 传入的device_id，设备号
        :param kwargs: 传入的
        :return: 返回该台空调的预设温度，室温，风向，风速，模式，
        '''
        data = '32F0D0B5FFFFFFFFFFFF2010A3C5000F34'
        result = self.samsung_requsets(data, kwargs['url'])
        if isinstance(result, dict):
            return result

        query_data = ''
        query_dict = {}
        # ac_all_info = result.replace(' ', '')[13:]
        ac_all_info = result.replace(' ', '')[12:]
        for i in range(0,48):
            ac_number = int('0x'+ac_all_info[:2], 16)
            if not i == ac_number:
                break
            if int(device_id[2:]) == ac_number:
                query_data = ac_all_info[2:22]
                break
            ac_all_info = ac_all_info[22:]

        wind_direction_data = int(bin(int(query_data[8:10], 16))[2:].zfill(8)[:5], 2)
        wind_direction = wind_direction_data not in SamsungAirConditionerDirection.values.keys() \
                         and 'stop' or SamsungAirConditionerDirection.values[wind_direction_data]

        wind_speed_data = int(bin(int(query_data[8:10], 16))[2:].zfill(8)[5:], 2)
        wind_speed = wind_speed_data not in SamsungAirConditionerSpeed.values.keys() \
                     and 'auto' or SamsungAirConditionerSpeed.values[wind_speed_data]

        mode_data = int(bin(int(query_data[10:12], 16))[2:].zfill(8)[3:6], 2)
        mode = mode_data not in SamsungAirConditionerMode.values.keys() \
               and 'auto' or SamsungAirConditionerMode.values[mode_data]

        if not query_data == '':
           query_dict = dict(temperature=int(query_data[:2], 16)-55,
                             room_temperature=int(query_data[2:4], 16)-55,
                             wind_direction=wind_direction.replace(' ','_'),
                             wind_speed=wind_speed.replace(' ','_'),
                             mode=mode.replace(' ','_'),
                             is_on=(bin(int(query_data[10:12], 16))[5:8]=='00' and False or True),
                             url=kwargs['url'])

        return query_dict

    def samsung_requsets(self, data, url):
        '''
        发送给三星服务器请求数据
        :param data:发送的信息
        :param url:三星空调本地服务器的路由
        :return:请求得到的数据
        '''
        # 请求头
        headers = {
            'Content-Type': 'application/json',
        }

        samsung_data = dict(data=data)
        try:
            post_result = requests.post(url, headers=headers, data=json.dumps(samsung_data).encode())
            if post_result.status_code == 400:
                return {"error": post_result.text}
            return post_result.text
        except Exception as e:
            return {"error": str(e)}

    def crc16_ccitt(self, data):
        '''CCITT CRC16 双C校验'''
        crc_data = bytes().fromhex(data)
        # a = CRCCCITT().calculate(crc_data)
        # s = hex(a).upper()[2:6].zfill(4)
        # crc16_data = s[:2] + ' ' + s[2:]
        return  crc_data
