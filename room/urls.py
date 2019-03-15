from django.conf.urls import url
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from room.views import (CheckinRoomView, CheckoutRoomView, ExtendRoomView, RoomNewCustomerView, RoomViewSet,
                        AddRoomTypeView, AddRoomView, AddEquipmentToHotelView, QueryHotelEquipmentView, ChangHotelStateView,
                        QueryRoomTypeEquipment, WXQueryEquipmentView)

router = DefaultRouter()
router.register(r'', RoomViewSet)

ht_room_v1_urlpatterns = [
    url(r'add_room_type', AddRoomTypeView.as_view(), name='add_room_type'),
    url(r'add_room', AddRoomView.as_view(), name='add_room'),
    url(r'add_equipment_to_hotel/', AddEquipmentToHotelView.as_view(), name='add_equipment_to_hotel'),
    url(r'query_hotel_eqipment/', QueryHotelEquipmentView.as_view(), name='query_hotel_eqipment'),
    url(r'change_hotel_state/', ChangHotelStateView.as_view(), name='change_hotel_state'),
    url(r'query_room_type_equipment/', QueryRoomTypeEquipment.as_view(), name='change_hotel_state'),
    url(r'^', include(router.urls))
]

zzj_room_v1_urlpatterns = [
    path(r'checkin/', CheckinRoomView.as_view(), name="checkin_room"),
    path(r'checkout/', CheckoutRoomView.as_view(), name="checkout_room"),
    path(r'extend/', ExtendRoomView.as_view(), name="extend_room"),
    path(r'new_customer/', RoomNewCustomerView.as_view(), name="room_new_customer"),
]

wx_room_v1_urlpatterns = [
    path(r'query_equipment/', WXQueryEquipmentView.as_view(), name="query_room_equipment"),
]
