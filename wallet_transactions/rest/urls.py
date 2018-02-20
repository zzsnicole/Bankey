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
    url(r'^api/create/$', CreateWallet.as_view(), name='create_wallet'),
    url(r'^api/balance/$', GetWalletBalance.as_view(), name='get_wallet_balance'),
    url(r'^api/pre_card_registration/$', PreCardRegistrationView.as_view(), name='pre_card_registration'),
    url(r'^api/card_registration/$', CardRegistrationView.as_view(), name='card_registration'),
]
