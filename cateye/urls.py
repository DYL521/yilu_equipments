from django.conf.urls import include, url

from cateye import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.CatEyeViewSet)

# The API URLs are now determined automatically by the router.
ht_cateye_v1_urlpatterns = [
    url(r'^', include(router.urls))
]

cateye_router = SimpleRouter()
cateye_router.register(r'software_version', views.CatEyeSoftwareVersionViewSet)

cateye_cateye_v1_urlpatterns = [
    url(r'update', views.CatEyeUpdateView.as_view(), name='cateye_update'),
    url(r'ping', views.CatEyePingView.as_view(), name='cateye_ping'),
    url(r'face_recognition', views.FaceRecognitionView.as_view(), name='face_recognition'),
    url(r'^', include(cateye_router.urls))
]
