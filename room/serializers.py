from django.utils.translation import ugettext as _

from customer.const import PMSChoices
from customer.models import Order, StayInfo
from rest_framework import serializers
from room.const import RoomStatus, EquipmentType, RoomOrRoomType
from room.models import Room, Hotel, RoomType, RoomTypeCommand, EquipmentCode
from light.models import Light
from electric_curtain.models import Curtain
from atomization_glass.models import Glass
from door.models import Lock
from equipment.const import ManufactureList
from air_conditioner.models import AirConditioner


class RoomCheckinSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    pms_type = serializers.IntegerField(write_only=True, help_text="Currently only 0 is allowed, for Lvyun")
    pms_id = serializers.CharField(write_only=True, help_text="ID on the PMS")
    start = serializers.DateTimeField(write_only=True, help_text="Time to start using this room")
    end = serializers.DateTimeField(write_only=True, help_text="Time expected to checkout")
    customer_ids = serializers.ListField(child=serializers.CharField(), min_length=1, write_only=True,
                                         help_text="A list of customer IDs, that are checked in together")

    def validate(self, data):
        available_pms_types = [x[0] for x in PMSChoices.choices]
        if data['pms_type'] not in available_pms_types:
            raise serializers.ValidationError(
                {"pms_type": _("only {} is allowed").format(available_pms_types)})

        room = Room.objects.get(hid=data['hid'], room_number=data['room_number'])
        if room.status != RoomStatus.available:
            raise serializers.ValidationError(
                {"room_number": _("This room is not available")})

        return data

    def create(self, validated_data):
        room = Room.objects.get(hid=validated_data['hid'], room_number=validated_data['room_number'])
        room.status = RoomStatus.inuse
        room.save()

        order = Order.objects.create(
            PMS_type=validated_data['pms_type'],
            PMS_ID=validated_data['pms_id'],
            start=validated_data['start'],
            end=validated_data['end'],
        )

        for customer_id in validated_data['customer_ids']:
            StayInfo.objects.create(
                order=order,
                customer_id=customer_id,
                room=room
            )

        return room


class RoomCheckoutSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def create(self, validated_data):
        room = Room.objects.get(hid=validated_data['hid'], room_number=validated_data['room_number'])
        room.status = RoomStatus.available
        room.save()

        stay_infos = StayInfo.objects.filter(room=room, is_active=True)
        stay_infos.update(is_active=False)

        return room


class RoomExtendSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    end = serializers.DateTimeField(write_only=True, help_text="Time expected to checkout")

    def validate(self, data):
        room = Room.objects.get(hid=data['hid'], room_number=data['room_number'])
        if room.status != RoomStatus.inuse:
            raise serializers.ValidationError(
                {"room_number": _("This room is not in use, can't extend")})

        stay_info_count = StayInfo.objects.filter(room=room, is_active=True).count()
        if stay_info_count <= 0:
            raise serializers.ValidationError(
                {"room_number": _("The order has expired, can't extend")})

        return data

    def create(self, validated_data):
        room = Room.objects.get(hid=validated_data['hid'], room_number=validated_data['room_number'])
        stay_info = StayInfo.objects.filter(room=room, is_active=True)
        order = stay_info[0].order

        order.end = validated_data['end']
        order.save()

        return room


class RoomNewCustomerSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    customer_ids = serializers.ListField(child=serializers.CharField(), min_length=1, write_only=True,
                                         help_text="A list of customer IDs, that are checked in together")

    def validate(self, data):
        room = Room.objects.get(hid=data['hid'], room_number=data['room_number'])
        if room.status != RoomStatus.inuse:
            raise serializers.ValidationError(
                {"room_number": _("This room is not in use, can't add new customer")})

        stay_info_count = StayInfo.objects.filter(room=room, is_active=True).count()
        if stay_info_count <= 0:
            raise serializers.ValidationError(
                {"room_number": _("The order has expired, can't add new customer")})

        return data

    def create(self, validated_data):
        room = Room.objects.get(hid=validated_data['hid'], room_number=validated_data['room_number'])
        stay_info = StayInfo.objects.filter(room=room, is_active=True)
        order = stay_info[0].order

        for customer_id in validated_data['customer_ids']:
            StayInfo.objects.create(
                order=order,
                customer_id=customer_id,
                room=room
            )

        return room


class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, data):
        hotel_instance = Hotel.objects.filter(hid=data['hid'], is_active=True)
        if hotel_instance:
            roomtype_instance = RoomType.objects.filter(id=data['room_type'].id)
            if not roomtype_instance:
                raise serializers.ValidationError(
                    {"room_type": _("room type does not exist")})

        else:
            raise serializers.ValidationError(
                {"hotel": _("hid does not exist")})

        return data


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('hid', 'is_active', 'bangqi_url', 'samsung_ac_url')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomTypeCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypeCommand
        fields = '__all__'


class QueryRoomTypeSerializer(serializers.Serializer):
    room_type_id = serializers.IntegerField(write_only=True, help_text="room type id")
    type = serializers.IntegerField(write_only=True,
                                    help_text="Devices that need to be added : 0, devices that have been added : 1")
    result = serializers.CharField(read_only=True, help_text="results of execution")
    light_list = serializers.DictField(read_only=True, help_text="A dict of light")
    curtain_list = serializers.DictField(read_only=True, help_text="A dict of curtain")
    atomizations_glass_list = serializers.DictField(read_only=True, help_text="A dict of atomizations glass")
    lock_list = serializers.DictField(read_only=True, help_text="A dict of lock")

    def validate(self, data):
        if not data['type'] in  [0, 1]:
            raise serializers.ValidationError(
                {"type": _("type not available")})

        light_type, curtain_type, atomizations_glass_type, lock_type, cateye_type, air_conditioner_type = \
            {}, {}, {}, {}, {}, {}
        light_list, curtain_list, atomizations_glass_list, lock_list, cateye_list, air_conditioner_list= \
            [], [], [], [], [], []
        room_type_instance = RoomType.objects.filter(id=data['room_type_id'])
        if not room_type_instance:
            raise serializers.ValidationError(
                dict(result="error", light_list={"type": "room_type","equipment_type":"light", "name":"灯","list": []},
                     curtain_list={"type": "room_type","equipment_type": "curtain", "name":"窗帘", "list": []},
                     atomizations_glass_list={"type": "room_type","equipment_type": "atomization glass",
                                              "name":"雾化玻璃", "list": []},
                     lock_list={"type": "room","equipment_type": "lock", "name":"门锁","list": []}))


        room_instance = Room.objects.filter(room_type=room_type_instance.first())

        for room_type_command_instance in RoomTypeCommand.objects.filter(room_type_id=data['room_type_id']):
            if EquipmentType.light == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], light_list, room_type_command_instance)
                if instance_dict:
                    light_type = instance_dict

            elif EquipmentType.curtain == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], curtain_list, room_type_command_instance)
                if instance_dict:
                    curtain_type = instance_dict

            elif EquipmentType.atomization_glass == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], atomizations_glass_list, room_type_command_instance)
                if instance_dict:
                    atomizations_glass_type = instance_dict

            elif EquipmentType.lock == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], lock_list, room_type_command_instance)
                if instance_dict:
                    lock_type = instance_dict

        if room_instance and data['type'] == 0:
            for room in room_instance:
                light_list.append(self.add_data(Light.objects.filter(room=room).values()))
                curtain_list.append(self.add_data(Curtain.objects.filter(room=room).values()))
                atomizations_glass_list.append(self.add_data(Glass.objects.filter(room=room).values()))
                lock_list.append(self.add_data(Lock.objects.filter(room=room).values()))

        if not light_type:
            light_type = {"type": "", "equipment_type": "light", "name": "灯",}

        if not curtain_type:
            curtain_type = {"type": "", "equipment_type": "curtain", "name": "窗帘",}

        if not atomizations_glass_type:
            atomizations_glass_type = {"type": "", "equipment_type": "atomization_glass", "name": "雾化玻璃",}
        data['result'] = 'success'
        data['light_list'] = dict(light_type, **dict(list=light_list))
        data['curtain_list'] = dict(curtain_type, **dict(list=curtain_list))
        data['atomizations_glass_list'] = dict(atomizations_glass_type, **dict(list=atomizations_glass_list))
        data['lock_list'] = dict(dict(type='room', equipment_type='lock', name='门锁'), **dict(list=lock_list))
        return data

    def add_data(self, equipment_data):
        for equipment in equipment_data:
            equipment['manufacture'] = ManufactureList.values[equipment['manufacture']]
            room_instance = Room.objects.get(id=equipment['room_id'])
            equipment['room_number'] = room_instance.room_number
            equipment['room_type'] = room_instance.room_type.room_type_name
            if 'room_type_command_id' in equipment.keys():
                room_type_equipment_instance = RoomTypeCommand.objects.get(
                    id=equipment['room_type_command_id']).equipment_name
                equipment['room_type_command'] = room_type_equipment_instance.code_name
                equipment['code'] = room_type_equipment_instance.code
        return equipment_data

    def not_increase(self, type, list_instance, equipment_instance):
        if not list_instance:
            type_dict = dict(type=RoomOrRoomType.values[equipment_instance.equipment_name.rt_rm].replace(' ','_'),
                             equipment_type=list(EquipmentType.labels.keys()) [list(EquipmentType.labels.values()).
                             index(EquipmentType.values[equipment_instance.equipment_name.equipment_type])],
                             name=EquipmentType.values[equipment_instance.equipment_name.equipment_type])
        else:
            type_dict = ''
        if type == 1:
            list_instance.append(dict(code=equipment_instance.equipment_name.code,
                                      code_name=equipment_instance.equipment_name.code_name,
                                      command=equipment_instance.command))
        return type_dict


class HotelStateSerializers(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    is_active = serializers.BooleanField(write_only=True, help_text="Has the hotel been removed")
    bangqi_url = serializers.CharField(default=None, help_text="bangqi hotel server url")
    samsung_ac_url = serializers.CharField(default=None, help_text="Air conditioner hotel server url")

    def validate(self, data):
        hotel_instance = Hotel.objects.filter(hid=data['hid'])
        if not hotel_instance:
            raise serializers.ValidationError({"hotel": _("hotel does not exists")})
        data['hotel_instance'] = hotel_instance
        return data

    def update(self, instance, validated_data):
        # bangqi_url和samsung_ac_url都没有传入的情况
        if validated_data['bangqi_url'] == None and validated_data['samsung_ac_url'] == None:
            instance.update(is_active=validated_data['is_active'])

        # bangqi_url和samsung_ac_url传入两个或者传入其中一个
        validated_data['bangqi_url'] == None and instance.update(
            is_active=validated_data['is_active'], samsung_ac_url=validated_data['samsung_ac_url']) \
        or (validated_data['samsung_ac_url'] == None and instance.update(
            is_active=validated_data['is_active'], bangqi_url=validated_data['bangqi_url'])) or instance.update(
            is_active=validated_data['is_active'], bangqi_url=validated_data['bangqi_url'],
            samsung_ac_url=validated_data['samsung_ac_url'])
        return validated_data


class GetQueryRoomTypeSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    result = serializers.CharField(read_only=True, help_text="results of execution")
    room_type_list = serializers.ListField(read_only=True, help_text="A list of curtain")

    def validate(self, data):
        data['room_type_list'] = []
        hotel_instance = Hotel.objects.filter(hid=data['hid'])
        if not hotel_instance:
            raise serializers.ValidationError({"hotel": _("hotel does not exists")})

        room_type_instance = RoomType.objects.filter(
            hotel_id=hotel_instance.first().id)
        if not room_type_instance:
            raise serializers.ValidationError({"room_type": _("room type does not exists")})
        for room_type in room_type_instance:
            data['room_type_list'].append(dict(id=room_type.id, room_type_name=room_type.room_type_name))
        data['result'] = 'success'
        return data


class GetQueryHotelEquipmentSerializer(QueryRoomTypeSerializer):
    room_type_id = serializers.IntegerField(required=False, help_text="room type id")
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")

    def validate(self, data):
        if not data['type'] in  [0, 1]:
            raise serializers.ValidationError(
                {"type": _("type not available")})

        light_list, curtain_list, atomizations_glass_list, lock_list = [], [], [], []
        hotel_instance = Hotel.objects.filter(hid=data['hid'])
        if not hotel_instance:
            raise serializers.ValidationError({"hotel": _("hotel does not exists")})

        room_type_instance = RoomType.objects.filter(hotel_id=hotel_instance.first().id)
        if not room_type_instance:
            raise serializers.ValidationError({"room_type": _("room type does not exists")})

        for room_type in room_type_instance:
            room_instance = Room.objects.filter(room_type=room_type)
            if room_instance:
                for room in room_instance:
                    light_list.append(self.add_data(Light.objects.filter(room=room).values()))
                    curtain_list.append(self.add_data(Curtain.objects.filter(room=room).values()))
                    atomizations_glass_list.append(self.add_data(Glass.objects.filter(room=room).values()))
                    lock_list.append(self.add_data(Lock.objects.filter(room=room).values()))
        data['result'] = 'success'
        data['light_list'] = dict(type='room_type', equipment_type='light', name='灯',list=light_list)
        data['curtain_list'] = dict(type='room_type', equipment_type='curtain', name='窗帘', list=curtain_list)
        data['atomizations_glass_list'] = dict(type='room_type', equipment_type='atomization glass',
                                               name='雾化玻璃', list=atomizations_glass_list)
        data['lock_list'] = dict(type='room', equipment_type='lock', name='门锁', list=lock_list)
        return data


class QueryHotelEquipmentSerializer(GetQueryHotelEquipmentSerializer):
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    def validate(self, data):
        if not data['type'] in  [0, 1]:
            raise serializers.ValidationError(
                {"type": _("type not available")})

        light_type, curtain_type, atomizations_glass_type, lock_type, cateye_type, air_conditioner_type = \
            {}, {}, {}, {}, {}, {}
        light_list, curtain_list, atomizations_glass_list, lock_list, cateye_list, air_conditioner_list= \
            [], [], [], [], [], []

        room_instance = Room.objects.filter(hid=data['hid'], room_number=data['room_number'])
        if not room_instance:
            raise serializers.ValidationError({"room": _("room does not exists")})

        for room_type_command_instance in RoomTypeCommand.objects.filter(room_type_id=room_instance.first().room_type_id):
            if EquipmentType.light == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], light_list, room_type_command_instance)
                if instance_dict:
                    light_type = instance_dict

            elif EquipmentType.curtain == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], curtain_list, room_type_command_instance)
                if instance_dict:
                    curtain_type = instance_dict

            elif EquipmentType.atomization_glass == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], atomizations_glass_list, room_type_command_instance)
                if instance_dict:
                    atomizations_glass_type = instance_dict

            elif EquipmentType.lock == room_type_command_instance.equipment_name.equipment_type:
                instance_dict = self.not_increase(data['type'], lock_list, room_type_command_instance)
                if instance_dict:
                    lock_type = instance_dict


        room = room_instance.first()
        if data['type'] == 0:
            light_list.append(self.add_data(Light.objects.filter(room=room).values()))
            curtain_list.append(self.add_data(Curtain.objects.filter(room=room).values()))
            atomizations_glass_list.append(self.add_data(Glass.objects.filter(room=room).values()))
            lock_list.append(self.add_data(Lock.objects.filter(room=room).values()))

        data['result'] = 'success'
        data['light_list'] = dict(light_type, **dict(list=light_list))
        data['curtain_list'] = dict(curtain_type, **dict(list=curtain_list))
        data['atomizations_glass_list'] = dict(atomizations_glass_type, **dict(list=atomizations_glass_list))
        data['lock_list'] = dict(dict(type='room', equipment_type='lock', name='门锁'), **dict(list=lock_list))
        return data


class GetAddRoomTypeSerializer(serializers.Serializer):
    result = serializers.CharField(read_only=True, help_text="results of execution")
    equipment_code_list = serializers.ListField(read_only=True, help_text="A list of equipment")

    def validate(self, data):
        equipment_code_list = []
        for code in EquipmentCode.objects.filter(is_active=True):
            equipment_code = dict(
                code=code.code,
                code_name=code.code_name
            )
            equipment_code_list.append(equipment_code)
        data['result'] = 'success'
        data['equipment_code_list'] = equipment_code_list
        return data


class AddRoomTypeSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_data = serializers.ListField(write_only=True, help_text="A list of room type")

    def validate(self, data):
        hotel_instance = Hotel.objects.filter(hid=data['hid'])
        if not hotel_instance:
            raise serializers.ValidationError({"hotel": _("hid does not exists")})
        data['hotel_instance'] = hotel_instance
        return data


class GetAddRoomSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    result = serializers.CharField(read_only=True, help_text="results of execution")
    room_type_list = serializers.ListField(read_only=True, help_text="A list of room type")
    manufacture_list = serializers.ListField(read_only=True, help_text="A list of manufacture")

    def validate(self, data):
        room_type_list, manufacture_list = [], []
        hotel_instance = Hotel.objects.filter(hid=data['hid'])
        if not hotel_instance:
            raise serializers.ValidationError({"hotel":_("hid does not exists")})

        room_type_instance = RoomType.objects.filter(hotel_id=hotel_instance.first())
        if not room_type_instance:
            raise serializers.ValidationError({"room_type":_("room type does not exists")})

        for room_type in room_type_instance:
            room_type_list.append(dict(id=room_type.id, room_type_name=room_type.room_type_name))

        for key, value in ManufactureList.values.items():
            manufacture_list.append(dict(name=key, code=value))
        data['result'] = 'success'
        data['room_type_list'] = room_type_list
        data['manufacture_list'] = manufacture_list
        return data


class GetAddEquipmentToHotelSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    result = serializers.CharField(read_only=True, help_text="results of execution")
    url = serializers.CharField(read_only=True, help_text="Hotel server url")
    equipment_list = serializers.ListField(read_only=True, help_text="A list of equipment")

    def validate(self, data):
        equipment_list = []
        relations_list = Hotel.objects.filter(hid=data['hid'])
        if not relations_list:
            raise serializers.ValidationError({"hotel": _("hid does not exists")})

        for relations in relations_list.first().equipmentcode_set.all():
            equipment_list.append(dict(name=relations.code_name, code=relations.code, type=relations.rt_rm,
                                       equipment_type=list(EquipmentType.labels.keys())[
                                           list(EquipmentType.values.keys()).index(relations.equipment_type)]))
        data['result'] = 'success'
        data['url'] = relations_list.first().url
        data['equipment_list'] = equipment_list
        return data


class WXQueryEquipmentSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def validate(self, data):
        room_instance = Room.objects.filter(hid__exact=data['hid'], room_number__exact=data['room_number'])
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['room_instance'] = room_instance.first()
        return data

    def equipment(self, data):
        equipment = []
        ac = AirConditioner.objects.filter(room = data['room_instance'], is_active=True)
        if ac:
            equipment.append('air_conditioner')

        ag = Glass.objects.filter(room = data['room_instance'], is_active=True)
        if ag:
            equipment.append('atomization_glass')

        light = Light.objects.filter(room = data['room_instance'], is_active=True)
        if light:
            equipment.append('light')

        curtain = Curtain.objects.filter(room = data['room_instance'], is_active=True)
        if curtain:
            equipment.append('curtain')

        lock = Lock.objects.filter(room=data['room_instance'], is_active=True)
        if lock:
            equipment.append('lock')
        return {'equipment' : equipment}
