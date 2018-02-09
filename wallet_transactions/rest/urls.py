from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet,\
                                                  GCMDeviceAuthorizedViewSet

from wallet_transactions.rest.views.wallet import *

router = routers.DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
