from rest_framework import response, status
from rest_framework.views import APIView
from electric_curtain.serializers import SwitchCurtainSerializer

# Create your views here.

class SwitchCurtainView(APIView):
    '''
    post:
    改变窗帘的状态，开窗帘或是关窗帘
    '''

    def get_serializer(self):
        return SwitchCurtainSerializer()

    def post(self, request, format=None):
        serializer = SwitchCurtainSerializer(data=request.data)
        if serializer.is_valid():
            curtain = serializer.validated_data['curtain_instance'].first()
            results = curtain.open_curtain(room_name=serializer.validated_data['room_number'],
                                           command=serializer.validated_data['command'],
                                           url=serializer.validated_data['url'])

            return response.Response(results, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
