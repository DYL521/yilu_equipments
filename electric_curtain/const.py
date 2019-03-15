from djchoices import ChoiceItem, DjangoChoices


class ControlTypeChoices(DjangoChoices):
    open_curtain = ChoiceItem(0)
    close_curtain = ChoiceItem(10)
