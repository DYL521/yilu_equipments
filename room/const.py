from djchoices import ChoiceItem, DjangoChoices


class RoomStatus(DjangoChoices):
    available = ChoiceItem(0)
    inuse = ChoiceItem(10)
    people_in = ChoiceItem(13)  # 房间内有人
    cleaning = ChoiceItem(20)
    maintaining = ChoiceItem(30)


class EquipmentType(DjangoChoices):
    light = ChoiceItem(0, '灯')
    curtain = ChoiceItem(10 , '窗帘')
    atomization_glass = ChoiceItem(20, '雾化玻璃')
    lock = ChoiceItem(30, '门锁')
    cateye = ChoiceItem(40, '猫眼')
    air_conditioner = ChoiceItem(50, '空调')

class RoomOrRoomType(DjangoChoices):
    room = ChoiceItem(0)
    room_type = ChoiceItem(1)
