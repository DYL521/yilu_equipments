from rest_framework import response, status
from rest_framework.views import APIView
from rest_framework import viewsets
from door.models import Door, DoorSensor, Lock, UserUnlockTime
from room.models import Room
from door.serializers import DoorSensorSerializer, DoorSerializer, LockSerializer, RemoteOpenLockSerializer, \
    UserCardSerializer, DeleteOpenUserSerializer, QueryOpenLockLogSerializer
from external_api import external_api_manager
import time


class DoorViewSet(viewsets.ModelViewSet):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    filter_fields = ('manufacture', 'is_active', 'is_opened')


class LockViewSet(viewsets.ModelViewSet):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    filter_fields = ('manufacture', 'is_active', 'is_opened')


class DoorSensorViewSet(viewsets.ModelViewSet):
    queryset = DoorSensor.objects.all()
    serializer_class = DoorSensorSerializer
    filter_fields = ('manufacture', 'is_active', 'is_opened')


class OpenLockView(APIView):
    """
    post:
    远程开门，可直接作为app开门接口调用.
    """

    def get_serializer(self):
        return RemoteOpenLockSerializer()

    def post(self, request, format=None):
        serializer = RemoteOpenLockSerializer(data=request.data)
        if serializer.is_valid():
            lock = serializer.validated_data['lock_instance'].first()
            results = lock.open_lock()
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClearUserView(APIView):
    """
    post:
    清空门锁
    """

    def get_serializer(self):
        return RemoteOpenLockSerializer()

    def post(self, request, format=None):
        serializer = RemoteOpenLockSerializer(data=request.data)
        if serializer.is_valid():
            lock = serializer.validated_data['lock_instance'].first()
            results = lock.clear_open_user()

            # 将能开房门的旅客设置为过期
            serializer.update(Room.objects.get(hid__exact=serializer.validated_data['hid'],
                                               room_number__exact=serializer.validated_data['room_number']),
                              serializer.validated_data)
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryLockStatusView(APIView):
    """
    post:
    查看门锁状态
    """

    def get_serializer(self):
        return RemoteOpenLockSerializer()

    def post(self, request, format=None):
        serializer = RemoteOpenLockSerializer(data=request.data)
        if serializer.is_valid():
            lock = serializer.validated_data['lock_instance'].first()
            results = lock.query_lock_status()
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryMidcomListView(APIView):
    """
    查询网关列表
    """

    def get(self, request, manufacture, format=None):
        lock_manufacture = manufacture
        api = external_api_manager.receiver_functions[lock_manufacture]["__api_class__"]()
        receiver_name = "provide_{}".format('lock_query_midcom_list')
        post_info = ''
        results = getattr(api, receiver_name)(post_info)
        return response.Response(results, status=status.HTTP_201_CREATED)


class AddLockUserView(APIView):
    """
    post:
    添加开门用户，CardType，MF卡：1；身份证 Id：2；密码：3
    """

    def get_serializer(self):
        return UserCardSerializer()

    def post(self, request, format=None):
        serializer = UserCardSerializer(data=request.data)
        if serializer.is_valid():
            lock = serializer.validated_data['lock_instance'].first()
            results = lock.add_lock_user(CardType=serializer.validated_data['CardType'],
                                             CardData=serializer.validated_data['CardData'],
                                             BeginTime=serializer.validated_data['BeginTime'],
                                             EndTime=serializer.validated_data['EndTime'])
            serializer.save()
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    """
    post:
    删除开门用户
    """

    def get_serializer(self):
        return DeleteOpenUserSerializer()

    def post(self, request, format=None):
        serializer = DeleteOpenUserSerializer(data=request.data)
        if serializer.is_valid():
            lock = serializer.validated_data['lock_instance'].first()
            results = lock.delete_user(CardType=serializer.validated_data['CardType'],
                                         CardData=serializer.validated_data['CardData'])

            serializer.update(Room.objects.get(hid__exact=serializer.validated_data['hid'],
                                               room_number__exact=serializer.validated_data['room_number']),
                              serializer.validated_data)
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryMidcomView(APIView):
    """
    post:
    查询网络盒状态
    """

    def get(self, request, manufacture, midcomno, format=None):
        lock_manufacture = manufacture
        api = external_api_manager.receiver_functions[lock_manufacture]["__api_class__"]()
        receiver_name = "provide_{}".format('midcom_status')
        post_info = dict(MidComNo=midcomno)
        results = getattr(api, receiver_name)(post_info)
        return response.Response(results, status=status.HTTP_201_CREATED)


class QueryLocklogView(APIView):
    """
    post:
    查询开锁日志
    """

    def get_serializer(self):
        return QueryOpenLockLogSerializer()

    def post(self, request, format=None):
        serializer = QueryOpenLockLogSerializer(data=request.data)
        if serializer.is_valid():
            BeginTime = serializer.validated_data['BeginTime'].strftime('%Y-%m-%d %H:%M:%S'),
            EndTime = serializer.validated_data['EndTime'].strftime('%Y-%m-%d %H:%M:%S')
            lock = serializer.validated_data['lock_instance'].first()
            data = lock.query_lock_log(BeginTime=BeginTime, EndTime=EndTime)
            return response.Response(data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersCanOpenDoorView(APIView):
    """
    post:
    查询此时这些方式可以开这间门
    """

    def get_serializer(self):
        return RemoteOpenLockSerializer()

    def post(self, request, format=None):
        serializer = RemoteOpenLockSerializer(data=request.data)
        if serializer.is_valid():
            results = []
            instance = Room.objects.get(hid__exact=serializer.validated_data['hid'],
                                        room_number__exact=serializer.validated_data['room_number'])
            open_info = UserUnlockTime.objects.filter(room__exact=instance, is_active=True).values()
            for open_data in open_info:
                if time.time() < time.mktime(open_data['end_time'].timetuple()):
                    results.append(open_data)
            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
