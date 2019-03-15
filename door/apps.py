from django.apps import AppConfig

from external_api.signals import lockserver_returns_informations


class DoorAppConfig(AppConfig):
    name = 'door'

    def ready(self):
        from door.signal_receivers import lockserver_returns_informations_receiver
        lockserver_returns_informations.connect(lockserver_returns_informations_receiver)



