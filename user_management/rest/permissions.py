from rest_framework.permissions import BasePermission

class IsTellerUser(BasePermission):
    """
    Permission on teller_service_charges will allow if user is owner/teller of those services.
    """

    def has_object_permission(self, request, view, obj):

        return obj.teller.user == request.user