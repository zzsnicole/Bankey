from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.http import Http404

from user_management.models import *
from .serializers import *
from .permissions import *

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List users and Retrieve user for admin only
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk):
        try:
            serializer = UserSerializer(User.objects.get(pk=pk, status='A'))
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


class Signup(generics.CreateAPIView):
    """
    Signup
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    User details, update user and delete user
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class Login(APIView):
    """
    Login
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        user = authenticate(request, email=request.data['email'],
                            password=request.data['password'])
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'message': 'Successfully login'
            })
        else:
            return Response({
                'success': False,
                'message': 'Fail to login'
            })


class Logout(APIView):
    """
    Logout
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        logout(request)
        return Response({
            'success': True,
            'message': 'Successfully logout'
        })


class ChangePassword(APIView):
    """
    Change password
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        new_password = request.data['password']
        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)  # Important!
        return Response({
            'success': True,
            'message': 'Successfully password changed'
        })


class UserContactsViews(generics.ListCreateAPIView):
    """
    List and add contact for loggedin user
    """
    queryset = User.objects.filter(status='A')
    serializer_class = UserContactsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = request.user.contacts.filter(status='A')
        serializer = UserContactsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'], status='A')
            if user:
                request.user.contacts.add(user)
                return Response({
                'success': True,
                'message': 'Successfully Added'
                })
        except User.DoesNotExist:
            raise Http404


class ServiceViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, add, update and delete services for bankey by admin only
    """
    queryset = Service.objects.filter(status='A')
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminUser,)


class TellerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List tellers and Retrieve teller for admin only
    """
    queryset = Teller.objects.filter(user__status='A')
    serializer_class = TellerSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk):
        try:
            serializer = TellerSerializer(Teller.objects.get(pk=pk, user__status='A'))
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


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


class AddTeller(generics.CreateAPIView):
    """
    Add teller
    """
    queryset = Teller.objects.filter(user__status='A')
    serializer_class = TellerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            user = User.objects.get(email=request.data['email'], status='A')
            Teller.objects.create(user=user, service_activation=request.data['service_activation'])
            return Response({
                'success': True,
                'message': 'Teller successfully created'
            })
        except User.DoesNotExist:
            raise Http404


class ChangeTellerActivationMode(generics.UpdateAPIView):
    """
    Update teller's service activation mode
    """
    queryset = Teller.objects.filter(user__status='A')
    serializer_class = TellerSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        try:
            teller = Teller.objects.get(user__email=request.data['email'], user__status='A')
            teller.service_activation = request.data['service_activation']
            teller.save()
            return Response({
                'success': True,
                'message': 'Teller updated successfully'
            })
        except Teller.DoesNotExist:
            raise Http404


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

    def post(self, request, format=None):
        try:
            service = Service.objects.get(code=request.data['service_code'])
            TellerServiceCharges.objects.create(teller=request.user.teller, service=service,\
                                                min_charges=request.data['min_charges'], \
                                                max_charges=request.data['max_charges'])
            return Response({
                'success': True,
                'message': 'Successfully created'
            })
        except:
            return Response({
                'success': False,
                'message': 'Fail to create'
            })


    def put(self, request, format=None):
        try:
            teller_service_charge = TellerServiceCharges.objects.get(teller=request.user.teller,\
                                                                    service__code=request.data['service_code'])
            teller_service_charge.min_charges = request.data['min_charges']
            teller_service_charge.max_charges = request.data['max_charges']
            teller_service_charge.save()
            return Response({
                'success': True,
                'message': 'Service charges updated successfully'
            })
        except TellerServiceCharges.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):

        try:
            teller_service_charge = TellerServiceCharges.objects.get(teller=request.user.teller,\
                                                                    service__code=request.data['service_code'])
            teller_service_charge.delete()
            return Response({
                'success': True,
                'message': 'Service charges deleted successfully'
            })
        except TellerServiceCharges.DoesNotExist:
            raise Http404


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

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'], status='A')
            UserRatingsAndFeedback.objects.create(
                teller=request.user.teller,
                user=user,
                ratings=request.data['ratings'],
                feedback=request.data['feedback']
            )
            return Response({
            'success': True,
            'message': 'Successfully Added'
            })
        except User.DoesNotExist:
            raise Http404


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

    def post(self, request, *args, **kwargs):
        try:
            teller = Teller.objects.get(user__email=request.data['email'], user__status='A')
            TellerRatingsAndFeedback.objects.create(
                user=request.user,
                teller=teller,
                ratings=request.data['ratings'],
                feedback=request.data['feedback']
            )
            return Response({
            'success': True,
            'message': 'Successfully Added'
            })
        except Teller.DoesNotExist:
            raise Http404







