from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()

# The API URLs are now determined automatically by the router.
ht_equipment_v1_urlpatterns = [
    url(r'^', include(router.urls))
]
