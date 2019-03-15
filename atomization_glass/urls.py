from django.conf.urls import include, url

from atomization_glass import views
from rest_framework.routers import DefaultRouter

door_router = DefaultRouter()

ht_atomizations_glass_v1_urlpatterns = [
    url(r'^switch_glass/$', views.SwitchGlassView.as_view(), name="control_glass"),
    url(r'^', include(door_router.urls))
]

wx_atomizations_glass_v1_urlpatterns = [
    url(r'^switch_glass/$', views.SwitchGlassView.as_view(), name="control_glass")
]
