from rest_framework.permissions import BasePermission
from accounts.models import UserType


class HasCustomerPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.type == UserType.user.value


class HasAdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.type == UserType.admin.value