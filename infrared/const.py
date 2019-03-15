from djchoices import ChoiceItem, DjangoChoices


class InfraredPositionChoices(DjangoChoices):
    just_in_door = ChoiceItem(0)
    in_toilet = ChoiceItem(10)
    in_bed_room = ChoiceItem(20)
    other = ChoiceItem(100)
