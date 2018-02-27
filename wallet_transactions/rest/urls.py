from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet,\
                                                  GCMDeviceAuthorizedViewSet

from wallet_transactions.rest.views.wallet import *
from wallet_transactions.rest.views.online_transactions import *
from wallet_transactions.rest.views.offline_transactions import *

router = routers.DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/currencies/$', CurrencyListView.as_view(), name='list_currencies'),
    url(r'^api/create/$', CreateWallet.as_view(), name='create_wallet'),
    url(r'^api/balance/$', GetWalletBalance.as_view(), name='get_wallet_balance'),
    url(r'^api/pre_card_registration/$', PreCardRegistrationView.as_view(), name='pre_card_registration'),
    # url(r'^api/card_registration/$', CardRegistrationView.as_view(), name='card_registration'),
    url(r'^api/add/cash_request/$', CreateCashRequestView.as_view(), name='add_cash_request'),
    url(r'^api/cash_request/(?P<pk>[0-9]+)/$', CashRequestDetailView.as_view(), name='cash_request_details'),
    # url(r'^api/cash_transaction/$', CashTransactionView.as_view(), name='cash_transaction'),
    # url(r'^api/add_money_by_card/$', AddMoneyByCardView.as_view(), name='add_money_by_card'),
    # url(r'^api/send_money/$', TransferTransactionView.as_view(), name='send_money'),
]
