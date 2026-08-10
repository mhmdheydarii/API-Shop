from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType


class HasCustomerPermissions(UserPassesTestMixin):

    def test_func(self):
        if self.requset.user.is_authenticated:
            return self.request.user.type == UserType.user.value
