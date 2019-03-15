from external_api.base import ExternalAPIBase
from external_api.signals import lockserver_returns_informations
from rest_framework import response
from utils.redis import setRedis
from door.const import OpenMethodChoices
import requests
import re


class HaoLiShi(ExternalAPIBase):
    MANUFACTURE = "hao_li_shi"

    def receiver_main(self, request):
        result = "I've received {} from the manufacture".format(request.data)
        return result

    def receiver_callback(self, request):
        """After sending the request to the locked server, the locked server returns an XML, which is processed."""
        data = str(request.body, 'utf-8')
        try:
            RoomId = re.search(r'(?<=.{4}RoomId.{4})(.+?)(?=.{4}/RoomId.{4})', data).group()
            Application = re.search(r'(?<=.{4}application.{4})(.+?)(?=.{4}/application.{4})', data).group()
            Description = re.search(r'(?<=.{4}Description.{4})(.+?)(?=.{4}/Description.{4})', data).group()
            UploadTime_date = re.search(r'([0-9]+/[0-9]+/[0-9]+)', data).group()
            UploadTime_time = re.search(r'([0-9]+:[0-9]+:[0-9]+)', data).group()
            UploadTime = UploadTime_date + ' ' + UploadTime_time
        except Exception as e:
            return response.Response(f'Partial check results, callbacks do not need to be processed.{e}')
        lockserver_returns_informations.send(sender=self.__class__,
                                             RoomId=RoomId,
                                             Application=Application,
                                             Description=Description,
                                             UploadTime=UploadTime,
                                             )

    def provide_lock_open_lock(self, device_id, **kwargs):
        post_name = 'OpenLock_REQ'
        request_info = ['ResultID', 'Description']
        results = self.lock_requsets(post_name, {'RoomId': device_id}, request_info)
        # 将数据存入redis
        accept_data = self.redis_data(results, device_id, post_name, {'RoomId': device_id}, request_info)
        setRedis('DoorLock', results['Description'], accept_data)
        return results

    def provide_lock_clear_open_user(self, device_id, **kwargs):
        post_name = 'Clear_Openuser_REQ'
        request_info = ['ResultID', 'Description']
        results = self.lock_requsets(post_name, {'RoomId': device_id}, request_info)
        # 将数据存入redis
        accept_data = self.redis_data(results, device_id, post_name, {'RoomId': device_id}, request_info)
        setRedis('DoorLock', results['Description'], accept_data)
        return results

    def provide_lock_query_lock_status(self, device_id, **kwargs):
        post_name = 'QueryLockStatus_REQ'
        request_info = ['RoomId', 'LockOpenState']
        results = self.lock_requsets(post_name, {'RoomId': device_id}, request_info)
        return results

    def provide_lock_query_midcom_list(self, post_info):
        post_name = 'QuertMidCom_REQ'
        request_info = ['Count', 'MidComNo']
        results = self.lock_requsets(post_name, post_info, request_info)
        return results

    def provide_lock_add_lock_user(self, device_id, CardType, CardData, BeginTime, EndTime, **kwargs):
        post_name = 'Add_OpenUser_REQ'
        request_info = ['ResultID', 'Description']
        post_info = {'RoomId': device_id, 'CardType': CardType, 'CardData': CardData,
                     'BeginTime': BeginTime, 'EndTime': EndTime}
        results = self.lock_requsets(post_name, post_info, request_info)
        # 将数据存入redis
        accept_data = self.redis_data(results, device_id, post_name, post_info, request_info)
        setRedis('DoorLock', results['Description'], accept_data)
        return results

    def provide_lock_delete_user(self, device_id, CardType, CardData, **kwargs):
        post_name = 'Delete_Openuser_REQ'
        request_info = ['ResultID', 'Description']
        post_info = {'RoomId': device_id, 'CardType': CardType, 'CardData': CardData}
        results = self.lock_requsets(post_name, post_info, request_info)
        # 将数据存入redis
        accept_data = self.redis_data(results, post_info['RoomId'], post_name, post_info, request_info)
        setRedis('DoorLock', results['Description'], accept_data)
        return results

    def provide_midcom_status(self, post_info):
        post_name = 'QuertNetMidComStatus_REQ'
        request_info = ['MidComNo', 'State']
        results = self.lock_requsets(post_name, post_info, request_info)
        return results

    def provide_lock_query_lock_log(self, device_id, BeginTime, EndTime, **kwargs):
        post_name = 'QueryOpenLockLog_REQ'
        request_info = ['Count', 'OpRoomType', 'OpRoomData', 'OpRoomDateTime']
        results = self.lock_requsets(post_name, {'RoomId': device_id, 'BeginTime': BeginTime[0], 'EndTime': EndTime},
                                     request_info)
        PasswordOP_list = []
        RoomCardOP_list = []
        CloseDoor_list = []
        try:
            for i in range(int(results['Count'][0])):
                RoomwordOP_dict = {}
                RoomCardOP_dict = {}
                CloseDoor_dict = {}

                if results['OpRoomType'][i] == str(OpenMethodChoices.password_open_door):
                    RoomwordOP_dict['OpRoomData'] = results['OpRoomData'][i]
                    RoomwordOP_dict['OpRoomDateTime'] = results['OpRoomDateTime'][i]
                    PasswordOP_list.append(RoomwordOP_dict)
                elif results['OpRoomType'][i] == str(OpenMethodChoices.card_open_door):
                    RoomCardOP_dict['OpRoomData'] = results['OpRoomData'][i]
                    RoomCardOP_dict['OpRoomDateTime'] = results['OpRoomDateTime'][i]
                    RoomCardOP_list.append(RoomCardOP_dict)
                elif results['OpRoomType'][i] == str(OpenMethodChoices.close_door):
                    CloseDoor_dict['OpRoomData'] = results['OpRoomData'][i]
                    CloseDoor_dict['OpRoomDateTime'] = results['OpRoomDateTime'][i]
                    CloseDoor_list.append(CloseDoor_dict)

        except Exception as e:
            return {"error": str(e)}

        data = dict(
            Count=results['Count'],
            PasswordOP=PasswordOP_list,
            RoomCardOP=RoomCardOP_list,
            CloseDoor=CloseDoor_list,
        )
        return data

    def lock_requsets(self, post_name, post_info, request_info):
        '''
        发送给网络锁平台的xml请求数据
        :param post_name:定义请求的名称
        :param post_info:请求的参数标签
        :return:request_info列表匹配的数据
        '''
        # 请求头
        headers = {
            'Content-Type': 'text/xml',
        }

        # 网络锁平台url
        url = "http://47.99.84.59:8005/NetLockWebServer.asmx"

        post_str = ''
        # 拼接请求
        for info in post_info:
            post_str += f'&lt;{info}&gt;{post_info[info]}&lt;/{info}&gt;'
        try:
            data = f'''<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body>
            <NetLockWeb xmlns="http://tempuri.org/"><recdatastr>&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;Command
            name="{post_name}" sn="6" version="1.0.0"&gt;{post_str}&lt;/Command&gt;</recdatastr></NetLockWeb></soap:Body>
            </soap:Envelope>'''
            # 发送请求得到数据
            haolishi_data = requests.post(url, headers=headers, data=data).text
            request_data = {}

            # 正则解析数据
            if post_name != 'QueryOpenLockLog_REQ' and post_name != 'QueryLockStatus_REQ':
                for req_info in request_info:
                    request_data[str(req_info)] = \
                        re.findall(r'(?<=.{4}' + req_info + '.{4})(.+?)(?=.{4}/' + req_info + '.{4})', haolishi_data)[0]

                if 'ResultID' in request_info:
                    if request_data['ResultID'] == '0':
                        request_data['Result'] = 'Messaged server succeed'
                    else:
                        request_data['Result'] = 'Message send server failed'
                return request_data

            else:
                for req_info in request_info:
                    request_data[str(req_info)] = \
                        re.findall(r'<' + req_info + '>(.*?)</' + req_info + '>',
                                   haolishi_data.replace("&lt;", "<").replace("&gt;", ">").replace("\n", ""))
                return request_data

        except Exception as e:
            return {"error": str(e)}

    def redis_data(self, results, post_RoomId, post_name, post_info, request_info):
        accept_data = dict(
            results,
            room_number=post_RoomId,
            post_name=post_name,
            post_info=post_info,
            request_info=request_info,
            time=0,
        )
        return accept_data
