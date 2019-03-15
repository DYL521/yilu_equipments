from air_conditioner.models import AirConditioner
from air_conditioner.serializers import AirConditionerSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from air_conditioner.serializers import (ChangeModeSerializer, ACSwitchSerializer, ChangeDirectionSerializer,
                                         ChangeSpeedSerializer, ChangeTemperatureSerializer, ACCommonSerializer)
from rest_framework import response, status
from air_conditioner.const import AirConditionerModeChoices, WindDirectionChoices, WindSpeedChoices


class AirConditionerViewSet(viewsets.ModelViewSet):
    queryset = AirConditioner.objects.all()
    serializer_class = AirConditionerSerializer
    filter_fields = ('manufacture', 'is_active', 'is_on')


class ChangeModeView(APIView):
    '''
    post:
    改变空调的模式
    '''
    def get_serializer(self):
        return ChangeModeSerializer()

    def post(self, request, format=None):
        serializer = ChangeModeSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            if 'error' not in query_data.keys():
                query_data['mode'] = AirConditionerModeChoices.values[serializer.validated_data['mode']]
                serializer.update(air_conditioner, dict(serializer.validated_data, **query_data))
                result_data =  air_conditioner.change_mode(**query_data)
                return response.Response(result_data, status=status.HTTP_201_CREATED)

            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ACSwitchView(APIView):
    def get_serializer(self):
        return ACSwitchSerializer()

    def post(self, request, format=None):
        serializer = ACSwitchSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            if 'error' not in query_data.keys():
                query_data['is_on'] = serializer.validated_data['switch']
                serializer.update(air_conditioner, dict(serializer.validated_data, **query_data))
                result_data =  air_conditioner.change_mode(**query_data)
                return response.Response(result_data, status=status.HTTP_201_CREATED)

            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeDirectionView(APIView):
    def get_serializer(self):
        return ChangeDirectionSerializer()

    def post(self, request, format=None):
        serializer = ChangeDirectionSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            if 'error' not in query_data.keys():
                query_data['wind_direction'] = WindDirectionChoices.values[serializer.validated_data['wind_direction']]
                serializer.update(air_conditioner, dict(serializer.validated_data, **query_data))
                result_data =  air_conditioner.change_mode(**query_data)
                return response.Response(result_data, status=status.HTTP_201_CREATED)

            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeSpeedView(APIView):
    def get_serializer(self):
        return ChangeSpeedSerializer()

    def post(self, request, format=None):
        serializer = ChangeSpeedSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            if 'error' not in query_data.keys():
                query_data['wind_speed'] = WindSpeedChoices.values[serializer.validated_data['wind_speed']]
                serializer.update(air_conditioner, dict(serializer.validated_data, **query_data))
                result_data =  air_conditioner.change_mode(**query_data)
                return response.Response(result_data, status=status.HTTP_201_CREATED)

            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeTemperatureView(APIView):
    def get_serializer(self):
        return ChangeTemperatureSerializer()

    def post(self, request, format=None):
        serializer = ChangeTemperatureSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            if 'error' not in query_data.keys():
                query_data['temperature'] = serializer.validated_data['temperature']
                serializer.update(air_conditioner, dict(serializer.validated_data, **query_data))
                result_data =  air_conditioner.change_mode(**query_data)
                return response.Response(result_data, status=status.HTTP_201_CREATED)

            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryACView(APIView):
    def get_serializer(self):
        return ACCommonSerializer()

    def post(self, request, format=None):
        serializer = ACCommonSerializer(data=request.data)
        if serializer.is_valid():
            air_conditioner = serializer.validated_data['air_conditioner_instance'].first()
            query_data = air_conditioner.query(url=serializer.validated_data['url'])
            result = serializer.convert_enum(query_data)
            if 'error' not in query_data.keys():
                return response.Response(result, status=status.HTTP_201_CREATED)
            return response.Response(query_data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
