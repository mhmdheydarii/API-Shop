from rest_framework.permissions import BasePermission
from accounts.models import UserType


class HasCustomerPermissions(BasePermission):

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:     
            return False
        return request.user.type == UserType.user.value
        
    
