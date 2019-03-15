from rest_framework import response, status
from rest_framework.views import APIView
from atomization_glass.serializers import SwitchGlassSerializer

# Create your views here.


class SwitchGlassView(APIView):
    '''
    post:
    改变雾化玻璃的状态，透明或是雾化镜面
    '''

    def get_serializer(self):
        return SwitchGlassSerializer()

    def post(self, request, format=None):
        serializer = SwitchGlassSerializer(data=request.data)
        if serializer.is_valid():
            glass = serializer.validated_data['glass_instance'].first()
            results = glass.switch_glass(room_name = serializer.validated_data['room_number'],
                                         command = serializer.validated_data['command'],
                                         url=serializer.validated_data['url'])

            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
