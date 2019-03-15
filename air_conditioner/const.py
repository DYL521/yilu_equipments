from djchoices import ChoiceItem, DjangoChoices


class AirConditionerModeChoices(DjangoChoices):
    not_sure = ChoiceItem(0)
    auto = ChoiceItem(10)
    cold = ChoiceItem(20)
    dehumidification = ChoiceItem(30)
    fan = ChoiceItem(40)
    warm = ChoiceItem(50)


class WindDirectionChoices(DjangoChoices):
    not_sure = ChoiceItem(0)
    up_and_down = ChoiceItem(10)
    left_and_right = ChoiceItem(20)
    around = ChoiceItem(30)
    stop = ChoiceItem(40)


class WindSpeedChoices(DjangoChoices):
    not_sure = ChoiceItem(0)
    auto = ChoiceItem(10)
    slow = ChoiceItem(20)
    medium = ChoiceItem(30)
    quick = ChoiceItem(40)
