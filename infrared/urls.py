from django.conf.urls import include, url

from infrared import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.InfraredViewSet)

# The API URLs are now determined automatically by the router.
ht_infrared_v1_urlpatterns = [
    url(r'^', include(router.urls))
]
