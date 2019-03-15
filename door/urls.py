from django.conf.urls import include, url

from door import views
from rest_framework.routers import DefaultRouter

door_router = DefaultRouter()
door_router.register(r'', views.DoorViewSet)

ht_door_v1_urlpatterns = [
    url(r'^', include(door_router.urls))
]

lock_router = DefaultRouter()

ht_lock_v1_urlpatterns = [
    url(r'open_lock', views.OpenLockView.as_view(), name='open_lock'),
    url(r'clear_open_user', views.ClearUserView.as_view(), name='clear_open_user'),
    url(r'query_lock_status', views.QueryLockStatusView.as_view(), name='query_lock_status'),
    url(r'query_midcom_list/(?P<manufacture>.+)/', views.QueryMidcomListView.as_view(), name='query_midcom_list'),
    url(r'add_lock_user', views.AddLockUserView.as_view(), name='add_lock_user'),
    url(r'delete_user', views.DeleteUserView.as_view(), name='delete_user'),
    url(r'midcom_status/(?P<manufacture>.+)/(?P<midcomno>.+)/', views.QueryMidcomView.as_view(), name='midcom_status'),
    url(r'query_lock_log', views.QueryLocklogView.as_view(), name='query_lock_log'),
    url(r'users_can_open_door', views.UsersCanOpenDoorView.as_view(), name='users_can_open_door'),
    url(r'', include(lock_router.urls))
]

wx_lock_v1_urlpatterns = [
    url(r'open_lock', views.OpenLockView.as_view(), name='open_lock'),
    url(r'', include(lock_router.urls))
]


doorsensor_router = DefaultRouter()
doorsensor_router.register(r'', views.DoorSensorViewSet)

ht_doorsensor_v1_urlpatterns = [
    url(r'^', include(doorsensor_router.urls))
]
