from django.conf.urls import url, include

from rest_framework import routers

from user_management.rest.views.user import *
from user_management.rest.views.teller import *

router = routers.DefaultRouter()
router.register(r'teller/services', TellerServiceChargesViewSet, base_name='teller_services')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/listcountries/$', CountryListView.as_view(), name='list_countries'),
    url(r'^api/signup/$', Signup.as_view(), name='signup'),
    url(r'^api/forgotpasswordrequest/$', ForgotPasswordRequestView.as_view(), name='forgot_password_request'),
    url(r'^api/forgotpassword/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^api/login/$', Login.as_view(), name='login'),
    url(r'^api/changepassword/$', ChangePassword.as_view(), name='change_password'),
    url(r'^api/logout/$', Logout.as_view(), name='logout'),
    url(r'^api/uploadphoto/$', PhotoView.as_view(), name='upload_photo'),
    url(r'^api/verificationrequest/$', PhoneVerificationRequestView.as_view(), name='phone_verification_request'),
    url(r'^api/phoneverification/$', PhoneVerificationView.as_view(), name='phone_verification'),
    url(r'^api/userdetails/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^api/usercontacts/$', UserContactsViews.as_view(), name='user_contacts'),
    url(r'^api/userfeedback/$', TellerRatingsAndFeedbackViews.as_view(), name='user_feedback'),
    url(r'^api/teller/$', AddTeller.as_view(), name='add_teller'),
    url(r'^api/teller/activationmode/$', ChangeTellerActivationMode.as_view(),name='change_teller_activation_mode'),
    url(r'^api/teller/fee/$', ChangeTellerFee.as_view(),name='change_teller_fee'),
    url(r'^api/add/teller/location/$', AddTellerLocationView.as_view(), name='add_teller_location'),
    url(r'^api/searchtellers/$', SearchTellersView.as_view(), name='search_tellers'),
    url(r'^api/tellerdetails/(?P<pk>[0-9]+)/$', GetTellerDetailsView.as_view(), name='teller_details'),
    url(r'^api/teller/(?P<pk>[0-9]+)/directions/$', GetTellerDirection.as_view(), name='directions_from user_to_teller'),
    url(r'^api/tellerfeedback/$', UserRatingsAndFeedbackViews.as_view(), name='teller_feedback'),
]
