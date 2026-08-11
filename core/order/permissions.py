from rest_framework.permissions import BasePermission
from accounts.models import UserType


class HasCustomerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:     
            return user.type == UserType.user.value
    
