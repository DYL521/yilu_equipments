from django.apps import AppConfig

from external_api.signals import infrared_detected_human


class InfraredAppConfig(AppConfig):
    name = 'infrared'

    def ready(self):
        from infrared.signal_receivers import infrared_detected_human_receiver
        infrared_detected_human.connect(infrared_detected_human_receiver)
