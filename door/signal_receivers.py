from utils.redis import my_redis
from rest_framework import response
from external_api import external_api_manager
import json


def lockserver_returns_informations_receiver(sender, **kwargs):
    try:
        Application = kwargs['Application'],
        Description = kwargs['Description']
    except Exception as e:
        return e
    if Description == "发送失败":
        res = json.loads(my_redis.hget('DoorLock', Application[0]).decode('ascii').replace("'", "\""))

        # 得到发送失败的信息后，继续请求。
        if res['post_name'] == "Add_OpenUser_REQ" or res['post_name'] == "OpenLock_REQ" \
                or res['post_name'] == "Delete_Openuser_REQ" or res['post_name'] == "Clear_Openuser_REQ":

            if res['time'] == 3:
                res['end'] = 'The request failed'
                return response.Response('It could be network or server problems')

            # 失败后继续发送请求
            lock_manufacture = "hao_li_shi"
            api = external_api_manager.receiver_functions[lock_manufacture]["__api_class__"]()
            receiver_name = "lock_requsets"
            getattr(api, receiver_name)(res['post_name'], res['post_info'], res['request_info'])

            res['time'] = res['time'] + 1
            Description = Application[0]
            my_redis.hset('DoorLock', Description, res)
            
