from rest_framework import response, status, viewsets
from rest_framework.views import APIView
from room.serializers import (
    RoomCheckinSerializer, RoomCheckoutSerializer, RoomExtendSerializer, RoomNewCustomerSerializer, RoomSerializer,
    HotelSerializer, RoomTypeSerializer, RoomTypeCommandSerializer, QueryRoomTypeSerializer, HotelStateSerializers,
    GetQueryRoomTypeSerializer, GetQueryHotelEquipmentSerializer, QueryHotelEquipmentSerializer,
    GetAddRoomTypeSerializer, AddRoomTypeSerializer, GetAddRoomSerializer, GetAddEquipmentToHotelSerializer,
    WXQueryEquipmentSerializer)
from door.serializers import LockSerializer
from atomization_glass.serializers import GlassSerializer
from electric_curtain.serializers import CurtainSerializer
from light.serializers import LightSerializer
from room.const import EquipmentType, RoomStatus
from room.models import RoomTypeCommand, EquipmentCode, RoomType, Hotel, Room


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('hid', 'status', 'is_active')


class CheckinRoomView(APIView):
    """
    post:
    Notification when a new room is used.
    """

    def get_serializer(self):
        return RoomCheckinSerializer()

    def post(self, request, format=None):
        serializer = RoomCheckinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutRoomView(APIView):
    """
    post:
    Notification when a room is no longer used.
    """

    def get_serializer(self):
        return RoomCheckoutSerializer()

    def post(self, request, format=None):
        serializer = RoomCheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtendRoomView(APIView):
    """
    post:
    Notification when a room is extended.
    """

    def get_serializer(self):
        return RoomExtendSerializer()

    def post(self, request, format=None):
        serializer = RoomExtendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomNewCustomerView(APIView):
    """
    post:
    Notification when a new customer joined a room.
    """

    def get_serializer(self):
        return RoomNewCustomerSerializer()

    def post(self, request, format=None):
        serializer = RoomNewCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRoomTypeView(APIView):
    """
    post:
    add equipment code
    """
    def get(self, request, format=None):
        serializer = GetAddRoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error=serializer.errors), status=status.HTTP_200_OK)  # 400

    def post(self, request, format=None):
        serializer = AddRoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            room_type_data_list, room_type_command_data_list, raise_errors_list = [], [], []
            for room_type_data in serializer.validated_data["room_data"]:
                room_type_data['hotel'] = serializer.validated_data['hotel_instance'].first().id
                room_type_serializer = RoomTypeSerializer(data=room_type_data)
                if room_type_serializer.is_valid():
                    room_type_serializer.save()
                    room_type_data_list.append(room_type_serializer.data)
                else:
                    raise_errors_list.append(dict(room_type_error=room_type_serializer.errors))

                for room_type_command_data in room_type_data['room_type_command']:
                    room_type_command_data['room_type'] = room_type_serializer.data['id']
                    room_type_command_data['equipment_name'] = EquipmentCode.objects.get(
                        code=room_type_command_data['code'], is_active=True).id
                    room_type_command_serializer = RoomTypeCommandSerializer(data=room_type_command_data)
                    if room_type_command_serializer.is_valid():
                        room_type_command_serializer.save()
                        room_type_command_data_list.append(room_type_command_serializer.data)
                    else:
                        raise_errors_list.append(dict(room_type_command_error=room_type_command_serializer.errors))

            equipment_data = dict(result='success',
                                  room_type_data_list = room_type_data_list,
                                  room_type_command_data_list = room_type_command_data_list,
                                  raise_errors_list=raise_errors_list)
            return response.Response(equipment_data, status=status.HTTP_202_ACCEPTED)
        return response.Response(dict(result='error', error = serializer.errors), status=status.HTTP_200_OK) #400


class AddRoomView(APIView):
    """
    post:
    add room and equipment
    """

    def get(self, request, format=None):
        serializer = GetAddRoomSerializer(data=dict(hid=int(request.GET.get('hid').replace('/', ''))))
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error = serializer.errors), status=status.HTTP_200_OK)#400

    def post(self, request, format=None):
        add_room_success, add_equipment_success, raise_errors_list = [], [], []
        if request.data["room_list"]:
            for room_data in request.data["room_list"]:
                room_data['room']['status'] = RoomStatus.maintaining
                room_data['room']['room_type'] = room_data['room']['room_type_id']
                room_serializer = RoomSerializer(data=room_data['room'])
                if room_serializer.is_valid():
                    room_serializer.save()
                    add_room_success.append(room_serializer.data)
                else:
                    raise_errors_list.append(dict(room_serializer=room_serializer.errors))

                #添加设备
                room_type_instance = RoomType.objects.filter(
                    hotel_id=Hotel.objects.filter(hid=room_data['room']['hid']).first().id,
                    id=room_data['room']['room_type_id'],
                    is_active=True)

                if room_type_instance:
                    for equipment in RoomTypeCommand.objects.filter(room_type_id=room_type_instance.first().id):
                        equipment_info = dict(
                            manufacture=room_data['room']['equipment_manufacturer'],
                            manufacture_device_id='1',
                            room=room_data['room']['id'],
                            room_type_command=equipment.id
                        )
                        #创建雾化玻璃
                        if equipment.equipment_name.equipment_type == EquipmentType.atomization_glass:
                            glass_serializer = GlassSerializer(data=equipment_info)
                            if glass_serializer.is_valid():
                                glass_serializer.save()
                                add_equipment_success.append(glass_serializer.data)
                            else:
                                raise_errors_list.append(dict(glass_serializer=glass_serializer.errors))

                        #创建电动窗帘
                        if equipment.equipment_name.equipment_type == EquipmentType.curtain:
                            curtain_serializer = CurtainSerializer(data=equipment_info)
                            if curtain_serializer.is_valid():
                                curtain_serializer.save()
                                add_equipment_success.append(curtain_serializer.data)
                            else:
                                raise_errors_list.append(dict(curtain_serializer=curtain_serializer.errors))

                        #创建灯
                        if equipment.equipment_name.equipment_type == EquipmentType.light:
                            light_serializer = LightSerializer(data=equipment_info)
                            if light_serializer.is_valid():
                                light_serializer.save()
                                add_equipment_success.append(light_serializer.data)
                            else:
                                raise_errors_list.append(dict(light_serializer=light_serializer.errors))

                    # 创建锁
                    if room_data['lock']:
                        room_data['lock']['room_id'] = room_data['room']['id']
                        lock_serializer = LockSerializer(data=room_data['lock'])
                        if lock_serializer.is_valid():
                            lock_serializer.save()
                            add_equipment_success.append(lock_serializer.data)
                        else:
                            raise_errors_list.append(dict(lock_serializer=lock_serializer.errors))

                    # 创建猫眼
                    if room_data['cateye']:
                        pass

                    # 创建空调
                    if room_data['air_conditioner']:
                        pass

                else:
                    return response.Response(
                        dict(result='error', error = 'room type does not exist'), status=status.HTTP_200_OK)#400
        else:
            return response.Response(
                dict(result='error', error = 'room list does not exist'), status=status.HTTP_200_OK)#400

        return response.Response(dict(result='success',
                                      add_room_success = add_room_success,
                                      add_equipment_success = add_equipment_success,
                                      raise_errors_list = raise_errors_list), status=status.HTTP_202_ACCEPTED)


class AddEquipmentToHotelView(APIView):
    """
    post:
    add equipment to hotel
    """
    def get(self, request, format=None):
        serializer = GetAddEquipmentToHotelSerializer(data=dict(hid=int(request.GET.get('hid').replace('/', ''))))
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error=serializer.errors), status=status.HTTP_200_OK)  # 400

    def post(self, request, format=None):
        hotel_data_list, add_code_to_hotel = [], []
        hotel_serializer = HotelSerializer(data=request.data["hotel"])
        if hotel_serializer.is_valid():
            hotel_serializer.save()
            hotel_data_list.append(hotel_serializer.data)
        hotel_data_list.append(hotel_serializer.errors)

        hotel_instance = Hotel.objects.filter(hid=request.data['hotel']['hid']).first()
        if hotel_instance:
            for code in request.data['equipment_code']:
                code_instance = EquipmentCode.objects.filter(code=code['code']).first()
                if code_instance:
                    code_instance.equipment_hotel.add(hotel_instance)
                    add_code_to_hotel.append(code_instance.code_name)

            return response.Response(dict(result='success', hotel_data_list=hotel_data_list,
                                          add_code_to_hotel=add_code_to_hotel), status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error=f'hid does not exist or {hotel_data_list}'),
                                 status=status.HTTP_200_OK)


class QueryHotelEquipmentView(APIView):
    def get(self, request, format=None):
        if not request.GET.get('hid'):
            return response.Response(dict(result='error', error='/room/query_hotel_eqipment/hid=123'), status=status.HTTP_200_OK)  # 400
        serializer = GetQueryHotelEquipmentSerializer(data=dict(hid=int(request.GET.get('hid').replace('/', ''))))
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error = serializer.errors), status=status.HTTP_200_OK)#400

    def post(self, request, format=None):
        serializer = QueryHotelEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error=serializer.errors), status=status.HTTP_200_OK)#400


class QueryRoomTypeEquipment(APIView):
    def get(self, request, format=None):
        serializer = GetQueryRoomTypeSerializer(data=dict(hid=int(request.GET.get('hid').replace('/', ''))))
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(dict(
            result='error', error = serializer.errors), status=status.HTTP_200_OK)#400

    def post(self, request, format=None):
        serializer = QueryRoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=status.HTTP_200_OK)#400


class ChangHotelStateView(APIView):
    def get(self, request, format=None):
        return response.Response(Hotel.objects.all().values(), status=status.HTTP_200_OK)

    def post(self, request,format=None):
        serializer = HotelStateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.update(serializer.validated_data['hotel_instance'], serializer.validated_data)
            return response.Response(dict(result='success', hotel_data=request.data), status=status.HTTP_200_OK)
        return response.Response(dict(result='error', error='hid does not exist'), status=status.HTTP_200_OK)#400


class WXQueryEquipmentView(APIView):
    """
    post:
    通过hid,room_number, 返回给微信的首页面的设备
    """

    def get_serializer(self):
        return WXQueryEquipmentSerializer()

    def post(self, request, format=None):
        serializer = WXQueryEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.equipment(serializer.validated_data)
            return response.Response(result, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
