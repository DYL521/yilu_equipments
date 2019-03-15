from django.conf.urls import include, url

from air_conditioner import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'change_mode', views.ChangeModeView)
router.register(r'', views.AirConditionerViewSet)

# The API URLs are now determined automatically by the router.
ht_ac_v1_urlpatterns = [
    url(r'^mode/', views.ChangeModeView.as_view(), name='change_mode'),
    url(r'^switch/', views.ACSwitchView.as_view(), name='air_conditioner_switch'),
    url(r'^direction/', views.ChangeDirectionView.as_view(), name='change_wind_direction'),
    url(r'^speed/', views.ChangeSpeedView.as_view(), name='change_wind_speed'),
    url(r'^temperature/', views.ChangeTemperatureView.as_view(), name='change_temperature'),
    url(r'^', include(router.urls)),
]

wx_ac_v1_urlpatterns = [
    url(r'^mode/', views.ChangeModeView.as_view(), name='change_mode'),
    url(r'^switch/', views.ACSwitchView.as_view(), name='air_conditioner_switch'),
    url(r'^direction/', views.ChangeDirectionView.as_view(), name='change_wind_direction'),
    url(r'^speed/', views.ChangeSpeedView.as_view(), name='change_wind_speed'),
    url(r'^temperature/', views.ChangeTemperatureView.as_view(), name='change_temperature'),
    url(r'^query/', views.QueryACView.as_view(), name='query_air_conditioner'),
    url(r'^', include(router.urls)),
]
