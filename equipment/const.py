from djchoices import ChoiceItem, DjangoChoices


class ManufactureList(DjangoChoices):
    hao_li_shi = ChoiceItem(0, "hao_li_shi")
    bang_qi = ChoiceItem(10, "bang_qi")
    yilu = ChoiceItem(20, "yi lu")
    samsung_air_conditioner = ChoiceItem(30, "samsung_air_conditioner")
    dummy = ChoiceItem(9999999, "dummy")  # test only, keep this at the end of the list


class EquipmentList(DjangoChoices):
    light = ChoiceItem(0, "light")
    ventilator = ChoiceItem(10, "ventilator")
    atomization_glass = ChoiceItem(20, "atomization_glass")
    electric_curtain = ChoiceItem(30, "electric_curtain")
