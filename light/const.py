from djchoices import ChoiceItem, DjangoChoices


class LightPositionChoices(DjangoChoices):
    other = ChoiceItem(0)
    night_lamp = ChoiceItem(10, '夜灯')
    porch_lamp = ChoiceItem(20, '廊灯')
    toilet = ChoiceItem(30, '卫生间灯')
    bed_room_main = ChoiceItem(40, '主灯')
    by_wall_left = ChoiceItem(50, '左壁灯')
    by_wall_right = ChoiceItem(60, '右壁灯')
    sleep_mode = ChoiceItem(70, '睡眠')
