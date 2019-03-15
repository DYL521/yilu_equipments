from external_api.base import ExternalAPIBase
import requests
import re


class BangQi(ExternalAPIBase):
    MANUFACTURE = "bang_qi"

    def provide_curtain_open_curtain(self, device_id, **kwargs):
        results = self.bangqi_requsets(
            room_name=kwargs['room_name'], url=kwargs['url'], Command=kwargs['command'])
        return results

    def provide_curtain_close_curtain(self, device_id, **kwargs):
        results = self.bangqi_requsets(
            room_name=kwargs['room_name'], url=kwargs['url'], Command=kwargs['command'])
        return results

    def provide_light_switch_light(self, device_id, **kwargs):
        results = self.bangqi_requsets(
            room_name=kwargs['room_name'], url=kwargs['url'], Command=kwargs['command'])
        return results

    def provide_glass_switch_glass(self, device_id, **kwargs):
        results = self.bangqi_requsets(
            room_name=kwargs['room_name'], url=kwargs['url'], Command=kwargs['command'])
        return results

    def bangqi_requsets(self, room_name, url, Command):
        '''
        发送给邦奇客控平台的xml请求数据
        :param RoomName:房间的编号
        :param Password:密码
        :param Command:八进制命令
        :return:完整的xml请求
        '''
        #

        # 请求头
        headers = {
            'Content-Type': 'application/octet-stream',
        }

        try:
            data = f'''<Request> 
    	<Auth company="Dalitek" cseq="1" request_time="2015-10-15 13:55:00" token="8900bfee0745a190349856c9073436af" /> 
    	<Service business="ThirdControl" function="Control" /> 
    	<RequestData> 
    		<RoomName>{room_name}</RoomName> 
    		<Password>123456</Password> 
    		<Command>{Command}</Command> 
    	</RequestData> 
    </Request>'''
            # 拼接请求
            post_result = requests.post(url, headers=headers, data=data).text
            if re.findall(r'resultcode="(.*?)" resultmessage', post_result) == ['200'] and \
                    re.findall(r'resultmessage="(.*?)" />', post_result) == ['OK']:
                request_data = 'success'
            else:
                request_data = 'failed'

            return request_data
        except Exception as e:
            return f'error：{e}'
