from djchoices import ChoiceItem, DjangoChoices


class SamsungAirConditionerDirection(DjangoChoices):
    up_and_down = ChoiceItem(26)
    left_and_right = ChoiceItem(27)
    around = ChoiceItem(28)
    stop = ChoiceItem(31)

class SamsungAirConditionerSpeed(DjangoChoices):
    auto = ChoiceItem(0)
    slow = ChoiceItem(2)
    medium = ChoiceItem(4)
    quick = ChoiceItem(5)

class SamsungAirConditionerMode(DjangoChoices):
    auto = ChoiceItem(0)
    cold = ChoiceItem(1)
    dehumidification = ChoiceItem(2)
    fan = ChoiceItem(3)
    warm = ChoiceItem(4)
