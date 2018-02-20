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

from user_management.rest.serializers.teller import *
from user_management.rest.permissions import *
from user_management.models import *

logger = logging.getLogger("users_log")


class AddTeller(APIView):
    """
    Add teller
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            mangopay_user = NaturalUser.get(instance.mangopay_user_id)
            address = request.user.address
            # request.user.email = request.data['email']
            # request.user.name = request.data['name']
            # request.user.birth_date = request.data['birth_date']
            # request.user.save()
            address_data = request.data['address']
            address.line1 = address_data['line1']
            mangopay_user.address.address_line_1 = address_data['line1']
            address.line2 = address_data['line2']
            mangopay_user.address.address_line_2 = address_data['line2']
            address.city = address_data['city']
            mangopay_user.address.city = address_data['city']
            address.state = address_data['state']
            mangopay_user.address.region = address_data['state']
            address.country = Country.objects.get(code=address_data['country'])
            mangopay_user.address.country = address_data['country']
            if address_data['pin_code']:
                address.pin_code = int(address_data['pin_code'])
                mangopay_user.address.postal_code = int(address_data['pin_code'])
            else:
                address.pin_code = None
            address.save()
            mangopay_user.save()
            # card_detail = UserCardDetails.objects.get(user=request.user, currency__code=request.data['currency'],\
            #                                                                                     is_completed = False)
            # card_registration = CardRegistration.get(card_detail.mangopay_card_registration_id)
            # card_registration.registration_data = request.data['registration_data']
            # card_registration.save()
            # card_detail.is_completed = True
            # card_detail.save()
            Teller.objects.create(user=request.user, fee=request.data['fee'])
            count = Teller.objects.filter(user__status='A').count()
            logger.info("Teller role is assigned to {}.".format(user.phone_no))
            return Response({
                'success': True,
                'message': 'Teller successfully created',
                'data': {
                    'count': count
                }
            })
        except Exception as e:
            logger.exception("{}, error occured while adding teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while adding teller.',
                'data': {}
            })


# class SearchTellersView(generics.ListAPIView):
#     """
#     Search Teller by phone_no, country and service
#     """
#     serializer_class = TellerSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         queryset = Teller.objects.filter(user__status='A', service_activation=True)
#         phone_no = self.request.query_params.get('phone_no', None)
#         country = self.request.query_params.get('country', None)
#         service = self.request.query_params.get('service', None)
#         if phone_no is not None:
#             queryset = queryset.filter(user__phone_no='+'+phone_no.strip())
#             return queryset
#         if country is not None:
#             queryset = queryset.filter(user__address__country__code=country)
#
#         if service is not None:
#             teller_list = TellerServiceCharges.objects.filter(service__code=service).values_list('teller',flat=True)
#             queryset = queryset.filter(id__in=teller_list)
#         return queryset


class AddTellerLocationView(APIView):
    """
    Add a location of teller
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            teller = Teller.objects.get(user=request.user)
            print(">>>>>teller=",teller)
            teller.lat = decimal.Decimal(self.request.query_params.get('lat', None))
            teller.long = decimal.Decimal(self.request.query_params.get('long', None))
            teller.save()
            teller_serializer = TellerSerializer(teller)
            logger.info("New location added successfully for {} teller.".format(request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Successfully added a location of teller.',
                'data': teller_serializer.data
            })
        except Exception as e:
            logger.exception("{}, error occured while adding a location of teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while adding a location of teller.',
                'data':{}
            })


class SearchTellersView(APIView):
    """
    Return tellers to display on map
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            lat = decimal.Decimal(self.request.query_params.get('lat', None))
            long = decimal.Decimal(self.request.query_params.get('long', None))
            tellers = Teller.objects.filter(user__status='A', service_activation=True)
            print(">>>>>tellers=",tellers)
            nearest_tellers = []
            for teller in tellers:
                if teller.is_nearest((lat,long)):
                    teller_serializer = TellerSerializer(teller)
                    nearest_tellers.append(teller_serializer.data)
            return Response({
                'success': True,
                'message': 'Successfully displayed details.',
                'data': nearest_tellers
            })
        except Exception as e:
            logger.exception("{}, error occured while displaying teller details.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while displaying teller details.',
                'data':{}
            })


class GetTellerDetailsView(APIView):
    """
    Get teller details
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            teller = Teller.objects.get(user__phone_no=request.data['mobile_number'], service_activation=True)
            teller_serializer = TellerSerializer(teller)
            return Response({
                'success': True,
                'message': 'Successfully displayed details.',
                'data':teller_serializer.data
            })
        except Exception as e:
            logger.error("{}, error occured while displaying teller details.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while displaying teller details.',
                'data':{}
            })


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
            teller.service_activation = request.data['service_activation']
            teller.save()
            logger.info("Now activation mode is {} for {} teller.".format(teller.service_activation, request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Activation mode is successfully changed for teller.'
            })
        except Exception as e:
            logger.exception("{}, error occured while changing activation mode for teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while changing activation mode for teller.',
                'data': {}
            })


class ChangeTellerFee(generics.RetrieveUpdateAPIView):
    """
    Display and update teller's service fee
    """
    queryset = Teller.objects.filter(user__status='A')
    serializer_class = TellerSerializer
    permission_classes = (IsTellerUser,)

    def get(self, request, format=None):
        try:
            teller = Teller.objects.get(user=request.user)
            return Response({
                'success': True,
                'message': 'Successfully displayed.',
                'data': {
                    "Fee": teller.fee
                }
            })
        except Exception as e:
            logger.error("{}, error occured while displaying fee of a teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while displaying fee of a teller.',
                'data': {}
            })

    @transaction.atomic()
    def put(self, request, format=None):
        try:
            teller = Teller.objects.get(user=request.user)
            teller.fee = request.data['fee']
            teller.save()
            logger.info("Fee successfully updated for {} teller.".format(request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Fee is successfully changed for teller.'
            })
        except Exception as e:
            logger.exception("{}, error occured while changing fee of the teller.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while changing fee of the teller.',
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
