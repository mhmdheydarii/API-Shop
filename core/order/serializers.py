from rest_framework import serializers
from django.utils import timezone
from .models import OrderModel, CouponModel


class CheckOutSerializer(serializers.ModelSerializer):

    coupon = serializers.CharField(required=False)

    class Meta:
        model = OrderModel
        fields = ["full_name", "phone_number", "state", "city", "address", "zip_code", "coupon"]

    def validate(self, attrs):
        code = attrs.get("coupon")

        if not code:
            attrs["coupon"] = None
            return attrs

        user = self.context["request"].user
        coupon = None

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            raise serializers.ValidationError({"message":"Coupon doesn't exist"})

        if coupon:

            if user in coupon.used_by.all():
                raise serializers.ValidationError({"message":"Coupon has already been used by this user"})

            if coupon.used_by.count() >= coupon.max_limit_usage:
                raise serializers.ValidationError({"message":"Coupon usage limit has been reached"})

            if coupon.expired_date and coupon.expired_date <= timezone.now():
                raise serializers.ValidationError({"message":"Coupon has expired"})

        attrs["coupon"] = coupon
        return attrs
