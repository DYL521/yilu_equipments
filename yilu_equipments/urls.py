"""yilu_equipments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

from air_conditioner.urls import ht_ac_v1_urlpatterns, wx_ac_v1_urlpatterns
from cateye.urls import ht_cateye_v1_urlpatterns, cateye_cateye_v1_urlpatterns
from door.urls import (ht_door_v1_urlpatterns, ht_doorsensor_v1_urlpatterns, ht_lock_v1_urlpatterns,
                       wx_lock_v1_urlpatterns)
from infrared.urls import ht_infrared_v1_urlpatterns
from light.urls import ht_light_v1_urlpatterns, wx_light_v1_urlpatterns
from receiver import views as receiver_views
from rest_framework.documentation import include_docs_urls
from room.urls import ht_room_v1_urlpatterns, zzj_room_v1_urlpatterns, wx_room_v1_urlpatterns
from electric_curtain.urls import ht_electric_curtain_v1_urlpatterns, wx_electric_curtain_v1_urlpatterns
from atomization_glass.urls import ht_atomizations_glass_v1_urlpatterns, wx_atomizations_glass_v1_urlpatterns
from equipment.urls import ht_equipment_v1_urlpatterns

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'docs/', include_docs_urls(title='YiLu Equipment Document')),
    re_path(r'receiver/(?P<manufacture>.+)/(?P<name>.+)/', receiver_views.receiver_view),
    path(r'api/', include([
        path(r'zzj/', include([
            path(r'v1/', include([
                path(r'room/', include(zzj_room_v1_urlpatterns)),
            ])),
        ])),
        path(r'ht/', include([
            path(r'v1/', include([
                path(r'ac/', include(ht_ac_v1_urlpatterns)),
                path(r'ag/', include(ht_atomizations_glass_v1_urlpatterns)),
                path(r'door/', include(ht_door_v1_urlpatterns)),
                path(r'lock/', include(ht_lock_v1_urlpatterns)),
                path(r'door_sensor/', include(ht_doorsensor_v1_urlpatterns)),
                path(r'electric_curtain/', include(ht_electric_curtain_v1_urlpatterns)),
                path(r'infrared/', include(ht_infrared_v1_urlpatterns)),
                path(r'light/', include(ht_light_v1_urlpatterns)),
                path(r'room/', include(ht_room_v1_urlpatterns)),
                path(r'equipment/', include(ht_equipment_v1_urlpatterns)),
                path(r'cateye/', include(ht_cateye_v1_urlpatterns)),
            ])),
        ])),
        path(r'cateye/', include([
            path(r'v1/', include([
                path(r'cateye/', include(cateye_cateye_v1_urlpatterns)),
            ])),
        ])),
        path(r'wx/', include([
            path(r'v1/', include([
                path(r'ac/', include(wx_ac_v1_urlpatterns)),
                path(r'ag/', include(wx_atomizations_glass_v1_urlpatterns)),
                path(r'lock/', include(wx_lock_v1_urlpatterns)),
                path(r'electric_curtain/', include(wx_electric_curtain_v1_urlpatterns)),
                path(r'light/', include(wx_light_v1_urlpatterns)),
                path(r'room/', include(wx_room_v1_urlpatterns)),
            ])),
        ])),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
