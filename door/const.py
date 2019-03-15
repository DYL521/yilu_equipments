from djchoices import ChoiceItem, DjangoChoices


class DoorOpenDirectionChoices(DjangoChoices):
    not_sure = ChoiceItem(0)
    from_inside = ChoiceItem(10)
    from_outside = ChoiceItem(20)


class LockOpenMethodChoices(DjangoChoices):
    not_sure = ChoiceItem(0)
    hotel_card = ChoiceItem(10)
    ID_card = ChoiceItem(20)
    facial_recognization = ChoiceItem(30)
    password = ChoiceItem(40)


class ServerLockOpenMethodChoices(DjangoChoices):
    hotel_card = ChoiceItem(1)
    ID_card = ChoiceItem(2)
    password = ChoiceItem(3)


class OpenMethodChoices(DjangoChoices):
    password_open_door = ChoiceItem(48)
    card_open_door = ChoiceItem(49)
    close_door = ChoiceItem(50)
