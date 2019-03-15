from django.conf.urls import include, url

from light import views
from rest_framework.routers import DefaultRouter
from light.views import LightUpOrOffView, WXLightView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.LightViewSet)

# The API URLs are now determined automatically by the router.
ht_light_v1_urlpatterns = [
    url(r'^control_light/$', LightUpOrOffView.as_view(), name="light_up_off"),
    url(r'^', include(router.urls))
]

wx_light_v1_urlpatterns = [
    url(r'^control_light/$', LightUpOrOffView.as_view(), name="light_up_off"),
    url(r'^query/$', WXLightView.as_view(), name="query_light")
]
