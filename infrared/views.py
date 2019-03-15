from infrared.models import Infrared
from infrared.serializers import InfraredSerializer
from rest_framework import viewsets


class InfraredViewSet(viewsets.ModelViewSet):
    queryset = Infrared.objects.all()
    serializer_class = InfraredSerializer
    filter_fields = ('manufacture', 'is_active', 'human_detected')
