from django.conf.urls import include, url

from electric_curtain import views
from rest_framework.routers import DefaultRouter

door_router = DefaultRouter()

ht_electric_curtain_v1_urlpatterns = [
    url(r'^switch_curtain/$', views.SwitchCurtainView.as_view(), name="control_curtain"),
    url(r'^', include(door_router.urls))
]

wx_electric_curtain_v1_urlpatterns = [
    url(r'^switch_curtain/$', views.SwitchCurtainView.as_view(), name="control_curtain")
]
