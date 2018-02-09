import string,random,logging

from datetime import datetime,date
from django.conf import settings
from django.db import transaction
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView

from .serializers import *
from .permissions import *
from user_management.models import *
from wallet_transactions.models import *

from twilio.rest import Client

logger = logging.getLogger("users_log")


class CountryListView(generics.ListAPIView):
    """
    List countries
    """
    queryset = Country.objects.filter(status='A')
    serializer_class = CountrySerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            res = self.list(request, *args, **kwargs)
            logger.info("List of countries are successfully retrieved.")
            return Response({
                'success': True,
                'message': 'List of countries.',
                'data': res.data
            })
        except Exception as e:
            logger.error("{}, error occured while listing countries.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while listing countries.',
                'data':{}
            })


class Signup(generics.CreateAPIView):
    """
    Signup
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            user = self.create(request, *args, **kwargs)
            user.data['user_id'] = User.objects.get(phone_no=user.data['phone_no']).id
            user.data['count'] = User.objects.filter(status='A').count()
            logger.info("{} user is created successfully.".format(user.data['phone_no']))
            return Response({
                'success': True,
                'message': 'User successfully created.',
                'data':user.data
            })
        except Exception as e:
            logger.exception("{}, error occured while signup.".format(e))
            return Response({
                'success': False,
                'message': 'User fail to create.',
                'data':{}
            })


class PhotoView(UpdateAPIView):
    """
    Upload profile photo
    """
    serializer_class = PhotoSerializer

    @transaction.atomic()
    def put(self, request):
        try:
            user = User.objects.get(phone_no=request.data['phone_no'])
            serializer = PhotoSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                  'success': True,
                  'message': 'Successfully uploaded photo.',
                  'data': {}
                })
        except Exception as e:
            logger.exception("{}, error occured while uploading user photo.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while uploading user photo.',
                'data':{}
            })


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update user and delete user
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserSerializer
    permission_classes = (IsSelf,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        try:
            res = self.update(request, *args, **kwargs)
            logger.info("{} profile is updated successfully.".format(res.data['phone_no']))
            return Response({
                'success': True,
                'message': 'Successfully updated.',
                'data': res.data
            })
        except Exception as e:
            logger.exception("{}, error occured while updating user profile.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while updating user profile.',
                'data':{}
            })

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        try:
            res = self.partial_update(request, *args, **kwargs)
            logger.info("{} profile is updated successfully.".format(res.data['phone_no']))
            return Response({
                'success': True,
                'message': 'Successfully updated.',
                'data': res.data
            })
        except Exception as e:
            logger.error("{}, error occured while updating user profile.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while updating user profile.',
                'data':{}
            })

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])
            res = self.destroy(request, *args, **kwargs)
            logger.info("{} is deleted successfully.".format(user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully deleted.',
                'data': {}
            })
        except Exception as e:
            logger.error("{}, error occured while deleting user.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while deleting user.',
                'data':{}
            })


class Login(APIView):
    """
    Login
    """
    permission_classes = (AllowAny,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:

            user = authenticate(request, phone_no=request.data['mobile_number'],
                                password=request.data['password'])
            if user is not None:
                login(request, user)
                auth_token = Token.objects.get(user=user).key
                logger.info("{} is login successfully.".format(user.phone_no))
                count = User.objects.filter(status='A').count()
                return Response({
                    'success': True,
                    'message': 'Successfully login.',
                    'data':{
                        'user_id': request.user.id,
                        'count':count,
                        'auth_token': auth_token
                    }
                })
            else:
                logger.info("wrong credentials used in login.")
                return Response({
                    'success': False,
                    'message': 'Please check credentials.',
                    'data':{}
                })
        except Exception as e:
            logger.error("{}, error occured while login.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while login.',
                'data':{}
            })


class Logout(APIView):
    """
    Logout
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            phone_no = request.user.phone_no
            logout(request)
            logger.info("{} user is logout successfully.".format(phone_no))
            return Response({
                'success': True,
                'message': 'Successfully logout.',
                'data': {}
            })
        except Exception as e:
            logger.error("{}, error occured while logout.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while logout.',
                'data':{}
            })


class ChangePassword(APIView):
    """
    Change password
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            new_password = request.data['password']
            user = request.user
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)  # Important!
            logger.info("{} changed password successfully.".format(user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully password changed',
                'data': {}
            })
        except Exception as e:
            logger.error("{}, error occured while changing password.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while changing password.',
                'data':{}
            })


class PhoneVerificationRequestView(APIView):
    """
    Phone Verification request
    """

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            try:
                random_string = ''.join([random.choice(string.digits) for n in range(6)])
                verification = PhoneVerification.objects.get(phone_no=request.data['mobile_number'])
                if verification.status == 'V':
                    user = User.objects.get(phone_no=request.data['mobile_number'])
                    user_serializer = UserSerializer(user)
                    return Response({
                        'success': False,
                        'message': 'User Exist.',
                        'data': user_serializer.data
                    })
                else:
                    verification.code = random_string
                    verification.verified_on = timezone.now()
                    verification.save()
            except PhoneVerification.DoesNotExist:
                verification = PhoneVerification.objects.create(phone_no=request.data['mobile_number'],\
                                                                code = random_string)

            client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(verification.phone_no,
                body="From bankey, your verification code is {}".format(verification.code),
                from_=settings.TWILIO_PHONE_NUMBER)
            logger.info("Verification code successfully sent to {}.".format(verification.phone_no))

            return Response({
                    'success': True,
                    'message': 'Verification code successfully sent.',
                    'data': {}
                })
        except Exception as e:
            logger.error("{}, error occured while mobile verification.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while mobile verification.',
                'data':{}
            })


class ForgotPasswordRequestView(APIView):
    """
    Forgot password request
    """

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            try:
                User.objects.get(phone_no=request.data['mobile_number'])
                random_string = ''.join([random.choice(string.digits) for n in range(6)])
                verification, created = ForgotPasswordRequests.objects.get_or_create(phone_no=request.data['mobile_number'])
                verification.code = random_string
                verification.verified_on = timezone.now()
                verification.status = 'U'
                verification.save()
            except User.DoesNotExist:
                return Response({
                    'success': True,
                    'message': 'User does not exit.',
                    'data': {}
                })

            client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(verification.phone_no,
                body="From bankey, your verification code is {}".format(verification.code),
                from_=settings.TWILIO_PHONE_NUMBER)
            logger.info("Verification code successfully sent to {}.".format(verification.phone_no))

            return Response({
                    'success': True,
                    'message': 'Verification code successfully sent for forgot password.',
                    'data': {}
                })
        except Exception as e:
            logger.error("{}, error occured while mobile verification for forgot password.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while mobile verification for forgot password.',
                'data':{}
            })


class PhoneVerificationView(APIView):

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            verification_code = request.data['verification_code']
            if request.data['process'] == 'signup':
                verification = PhoneVerification.objects.get(phone_no=request.data['mobile_number'])
            else:
                verification = ForgotPasswordRequests.objects.get(phone_no=request.data['mobile_number'])
            if verification.code == verification_code:
                verification.status = 'V'
                verification.save()
                logger.info("Verification successfully completed for {}.".format(verification.phone_no))
                return Response({
                'success': True,
                'message': 'Successfully verified.',
                'data': {}
                })
            else:
                logger.info("Wrong verification code given for {}.".format(verification.phone_no))
                return Response({
                'success': False,
                'message': 'Fail to verified',
                'data': {}
                })
        except Exception as e:
            logger.error("{}, error occured while mobile verification.".format(e))
            return Response({
                'success': False,
                'message': 'Something goes wrong, please contact support team.',
                'data': {}
            })


class ForgotPasswordView(APIView):
    """
    Forgot password
    """

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            new_password = request.data['password']
            user = User.objects.get(phone_no=request.data['mobile_number'])
            user.set_password(new_password)
            user.save()

            logger.info("{} successfully changed password.".format(user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully password changed',
                'data': {}
            })
        except Exception as e:
            logger.error("{}, error occured while forgot password process.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while forgot password process.',
                'data':{}
            })


class UserContactsViews(generics.ListCreateAPIView):
    """
    List and add contact for logged-in user
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserContactsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = request.user.contacts.filter(status='A')
        serializer = UserContactsSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_no=request.data['mobile_number'], status='A')
            if user:
                request.user.contacts.add(user)
                logger.info("{} added into contacts of {} user.".format(user.phone_no, request.user.phone_no))
                return Response({
                'success': True,
                'message': 'Successfully Added',
                'data':{}
                })
        except Exception as e:
            logger.error("{}, error occured while adding contacts.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while adding contacts.',
                'data': {}
            })


class AddTeller(APIView):
    """
    Add teller
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            user = request.user
            address = request.user.address
            user.email = request.data['email']
            user.name = request.data['name']
            user.birth_date = request.data['birth_date']
            user.save()
            address_data = request.data['address']
            address.line1 = address_data['line1']
            address.line2 = address_data['line2']
            address.city = address_data['city']
            address.state = address_data['state']
            address.country = Country.objects.get(code=address_data['country'])
            address.pin_code = address_data['pin_code']
            address.save()
            Teller.objects.create(user=user)
            logger.info("Teller role is assigned to {}.".format(user.phone_no))
            return Response({
                'success': True,
                'message': 'Teller successfully created',
                'data': {}
            })
        except Exception as e:
            logger.exception("{}, error occured while adding teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while adding teller.',
                'data': {}
            })


class SearchTellersView(generics.ListAPIView):
    """
    Search Teller by phone_no, country and service
    """
    serializer_class = TellerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Teller.objects.filter(user__status='A', service_activation=True)
        phone_no = self.request.query_params.get('phone_no', None)
        country = self.request.query_params.get('country', None)
        service = self.request.query_params.get('service', None)
        if phone_no is not None:
            queryset = queryset.filter(user__phone_no=phone_no)
            return queryset
        if country is not None:
            queryset = queryset.filter(user__address__country=country)

        if service is not None:
            teller_list = TellerServiceCharges.objects.filter(service__code=service).values_list('teller',flat=True)
            queryset = queryset.filter(id__in=teller_list)
        return queryset


class ChangeTellerActivationMode(generics.RetrieveUpdateAPIView):
    """
    Display and update teller's service activation mode
    """
    queryset = Teller.objects.filter(user__status='A')
    serializer_class = TellerSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            teller = Teller.objects.get(user=request.user)
            logger.info("Now activation mode is {} for {} teller.".format(teller.service_activation, request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully displayed.',
                'data': {
                    "activation_mode": teller.service_activation
                }
            })
        except Exception as e:
            logger.error("{}, error occured while displaying activation mode for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while displaying activation mode for teller.',
                'data': {}
            })

    @transaction.atomic()
    def put(self, request, format=None):
        try:
            teller = Teller.objects.get(user=request.user)
            if request.data['service_activation'] == True:
                teller_service_charges = TellerServiceCharges.objects.filter(teller=teller)
                bank_details = UserBankInfo.objects.filter(user=request.user)
                if not teller_service_charges or not bank_details:
                    return Response({
                        'success': True,
                        'message': 'First add charges and bank details in your account.'
                    })

            teller.service_activation = request.data['service_activation']
            teller.save()
            logger.info("Now activation mode is {} for {} teller.".format(teller.service_activation, request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Activation mode is successfully changed for teller.'
            })
        except Exception as e:
            logger.error("{}, error occured while changing activation mode for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while changing activation mode for teller.',
                'data': {}
            })


class TellerServiceChargesViewSet(viewsets.ViewSet):
    """
    List, retrieve, add, update and delete Teller services
    """
    permission_classes = (IsTellerUser,)

    def list(self, request):
        queryset = TellerServiceCharges.objects.filter(teller__user=request.user)

        serializer = TellerServiceChargesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TellerServiceCharges.objects.filter(teller__user=request.user)
        teller_service_charge = get_object_or_404(queryset, pk=pk)
        serializer = TellerServiceChargesSerializer(teller_service_charge)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            service = Service.objects.get(code=request.data['service_code'])
            TellerServiceCharges.objects.create(teller=request.user.teller, service=service,\
                                                min_charges=request.data['min_charges'], \
                                                max_charges=request.data['max_charges'])
            logger.info("{} service created successfully for {} teller.".format(service.name, request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully created'
            })
        except Exception as e:
            logger.error("{}, error occured while creating service charges for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Fail to create service charges'
            })

    @transaction.atomic()
    def put(self, request, format=None):
        try:
            teller_service_charge = TellerServiceCharges.objects.get(teller=request.user.teller,\
                                                                    service__code=request.data['service_code'])
            teller_service_charge.min_charges = request.data['min_charges']
            teller_service_charge.max_charges = request.data['max_charges']
            teller_service_charge.save()
            logger.info("{} service updated successfully for {} teller.".format(request.data['service_code'],\
                                                                                request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Service charges updated successfully'
            })
        except Exception as e:
            logger.error("{}, error occured while updating service charges for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Fail to update service charges'
            })

    @transaction.atomic()
    def delete(self, request, format=None):

        try:
            teller_service_charge = TellerServiceCharges.objects.get(teller=request.user.teller,\
                                                                    service__code=request.data['service_code'])
            teller_service_charge.delete()
            logger.info("{} service deleted successfully for {} teller.".format(request.data['service_code'],\
                                                                                request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Service charges deleted successfully'
            })
        except Exception as e:
            logger.error("{}, error occured while deleting service charges for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Fail to delete service charges'
            })


class UserRatingsAndFeedbackViews(generics.ListCreateAPIView):
    """
    List and Add ratings and feedback from teller to user
    """
    queryset = UserRatingsAndFeedback.objects.filter(status='A')
    serializer_class = UserRatingsAndFeedbackSerializer
    permission_classes = (IsTellerUser,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserRatingsAndFeedbackSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_no=request.data['mobile_number'], status='A')
            UserRatingsAndFeedback.objects.create(
                teller=request.user.teller,
                user=user,
                ratings=request.data['ratings'],
                feedback=request.data['feedback']
            )
            logger.info("Feedback is given from {} teller to {} user.".format(request.user.phone_no, \
                                                                                user.phone_no))
            return Response({
            'success': True,
            'message': 'Successfully Added'
            })
        except Exception as e:
            logger.error("{}, error occured while sending feedback from teller to user.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while sending feedback from teller to user.'
            })


class TellerRatingsAndFeedbackViews(generics.ListCreateAPIView):
    """
    List and Add ratings and feedback from user to teller
    """
    queryset = TellerRatingsAndFeedback.objects.filter(status='A')
    serializer_class = TellerRatingsAndFeedbackSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TellerRatingsAndFeedbackSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            teller = Teller.objects.get(user__phone_no=request.data['mobile_number'], user__status='A')
            TellerRatingsAndFeedback.objects.create(
                user=request.user,
                teller=teller,
                ratings=request.data['ratings'],
                feedback=request.data['feedback']
            )
            logger.info("Feedback is given from {} user to {} teller.".format(request.user.phone_no, \
                                                                                teller.user.phone_no))
            return Response({
            'success': True,
            'message': 'Successfully Added'
            })
        except Exception as e:
            logger.error("{}, error occured while sending feedback from user to teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while sending feedback from user to teller.'
            })
