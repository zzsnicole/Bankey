"""Bankey URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework import routers
from user_management.rest.viewsets import *
from wallet_transactions.rest.viewsets import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tellers', TellerViewSet)
router.register(r'services', ServiceViewSet, base_name='services')
router.register(r'countries', CountryViewSet, base_name='countries')
router.register(r'tellerservices', TellerServiceChargesViewSet, base_name='tellerservices')
router.register(r'tellercashbalances', TellerCashBalancesViewSet, base_name='tellercashbalances')
router.register(r'currency', CurrencyViewSet, base_name='currencies')
router.register(r'wallets', WalletViewSet, base_name='wallets')
router.register(r'transactions', SendMoneyTransactionHistoryViews, base_name='transaction')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api/listcountries/$', CountryListView.as_view(), name='list_countries'),
    url(r'^api/signup/$', Signup.as_view(), name='signup'),
    url(r'^api/userdetails/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^api/usercontacts/$', UserContactsViews.as_view(), name='user_contacts'),
    url(r'^api/tellerfeedback/$', UserRatingsAndFeedbackViews.as_view(), name='teller_feedback'),
    url(r'^api/userfeedback/$', TellerRatingsAndFeedbackViews.as_view(), name='user_feedback'),
    url(r'^api/login/$', Login.as_view(), name='login'),
    url(r'^api/logout/$', Logout.as_view(), name='logout'),
    url(r'^api/changepassword/$', ChangePassword.as_view(), name='change_password'),
    url(r'^api/verificationrequest/$', PhoneVerificationRequestView.as_view(), name='phone_verification_request'),
    url(r'^api/phoneverification/$', PhoneVerificationView.as_view(), name='phone_verification'),
    url(r'^api/teller/activationmode/$', ChangeTellerActivationMode.as_view(),\
                                                            name='change_teller_activation_mode'),
    url(r'^api/walletbalance/$', ViewWalletBalance.as_view(), name='wallet_balance'),
    url(r'^api/searchtellers/$', SearchTellersView.as_view(), name='search_tellers'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)