from light.serializers import LightUpOrOffSerializer
from equipment.const import EquipmentList
from rest_framework import response, status
from rest_framework.views import APIView
from light.models import Light
from light.serializers import LightSerializer, WXLightSerializer
from rest_framework import viewsets

class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    filter_fields = ('manufacture', 'is_active', 'is_on')


class LightUpOrOffView(APIView):
    '''
    post:
    改变灯的状态，开灯或是关灯
    '''
    def get_serializer(self):
        return LightUpOrOffSerializer()

    def post(self, request, format=None):
        serializer = LightUpOrOffSerializer(data=request.data)
        if serializer.is_valid():
            light = serializer.validated_data['light_instance'].first()
            results = light.switch_light(room_name = serializer.validated_data['room_number'],
                                         command = serializer.validated_data['command'],
                                         url=serializer.validated_data['url'])

            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WXLightView(APIView):
    '''
    post:
    微信查询灯的数量接口
    '''
    def get_serializer(self):
        return WXLightSerializer()

    def post(self, request, format=None):
        serializer = WXLightSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.light(serializer.validated_data)
            return response.Response(result, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
