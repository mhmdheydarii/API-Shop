from rest_framework.permissions import BasePermission
from accounts.models import UserType


class HasAdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.type in (UserType.admin.value, UserType.superuser.value)
        

class HasCustomerPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.type == UserType.user.value