from django.db import models

from base.models import ActiveUpdateModelCommon
from room.const import RoomStatus, EquipmentType


class Hotel(ActiveUpdateModelCommon):
    hid = models.IntegerField(help_text="Hotel ID from EFD_set", unique=True)
    bangqi_url = models.URLField(null=True)
    samsung_ac_url = models.URLField(null=True)


class RoomType(ActiveUpdateModelCommon):
    id = models.IntegerField(primary_key=True)
    room_type_name = models.CharField(max_length=256)
    hotel = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING)


class Room(ActiveUpdateModelCommon):
    id = models.IntegerField(primary_key=True)
    hid = models.IntegerField(help_text="Hotel ID from EFD_set")
    room_number = models.CharField(max_length=16)
    room_type = models.ForeignKey(RoomType, on_delete=models.DO_NOTHING, null=True)
    floor = models.SmallIntegerField()
    status = models.PositiveSmallIntegerField(choices=RoomStatus.choices)

    def __str__(self):
        return self.room_number


class EquipmentCode(ActiveUpdateModelCommon):
    """设备种类及其对应属性

    code:设备对应的code码
    code_name:设备名称，例如：主灯，卫生间灯，窗帘，门锁等
    rt_rm:RoomType or Room 这个设备在房型中设置或是在房间中设置
    equipment_type:设备的类型 0:light, 10:curtain...
    hid_ecid:设备和酒店是多对多的关系
    """
    code = models.CharField(max_length=256)
    code_name = models.CharField(max_length=256)
    rt_rm = models.BooleanField()
    equipment_type = models.PositiveSmallIntegerField(choices=EquipmentType.choices)
    hid_ecid = models.ManyToManyField(to=Hotel, name='equipment_hotel')


class RoomTypeCommand(ActiveUpdateModelCommon):
    """房型（客控方案）下的命令
    部分客控厂商对相同客控方案的命令是相同的（传输时发送房间号和该房间对应的客控方案command命令即可）
    command:房型中的某种设备对应命令
    room_type:外键关联到房型
    equipment_name：外键关联到设备种类
    """
    command = models.CharField(max_length=256)
    room_type = models.ForeignKey(RoomType, on_delete=models.DO_NOTHING)
    equipment_name = models.ForeignKey(EquipmentCode, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('room_type', 'equipment_name')
