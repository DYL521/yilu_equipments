import logging

from cateye.models import CatEye, CatEyeSoftwareVersion
from cateye.serializers import (
    CatEyePingSerializer, CatEyeSerializer, CatEyeSoftwareVersionSerializer, CatEyeUpdateSerializer,
    FaceRecognitionSerializer)
from rest_framework import response, status, views, viewsets

logger = logging.getLogger(__name__)


class CatEyeViewSet(viewsets.ModelViewSet):
    queryset = CatEye.objects.all()
    serializer_class = CatEyeSerializer
    filter_fields = ('manufacture', 'is_active')


class CatEyeSoftwareVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatEyeSoftwareVersion.objects.all()
    serializer_class = CatEyeSoftwareVersionSerializer


class CatEyeUpdateView(views.APIView):
    serializer_class = CatEyeUpdateSerializer

    def post(self, request):
        serializer = CatEyeUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceRecognitionView(views.APIView):
    serializer_class = FaceRecognitionSerializer

    def post(self, request):
        logger.debug("got data: {}".format(request.data))
        serializer = FaceRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            result, detail = serializer.check_face()
            if result:
                logger.debug("face recognized, return success")
                return response.Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                logger.debug("face not recognized, return failed. Reason: {}".format(detail))
                return response.Response({"status": "failed", "detail": detail}, status=status.HTTP_200_OK)

        logger.debug("error in data from catey: {}".format(str(serializer.errors)))
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatEyePingView(views.APIView):
    serializer_class = CatEyePingSerializer

    def post(self, request):
        serializer = CatEyePingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
