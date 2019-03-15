from django.dispatch import Signal

infrared_detected_human = Signal(providing_args=["hid", "room_number", "position"])
lockserver_returns_informations = Signal(providing_args=["RoomId", "Application", "Description", "UploadTime"])

