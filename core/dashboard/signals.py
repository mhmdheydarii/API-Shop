from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from accounts.models import Profile, User
from order.models import OrderModel, CouponModel
from payment.models import PaymentModel
from shop.models import ProductModel, CategoryModel
from website.models import TicketModel


# Admin dashboard cache
@receiver([post_save, post_delete], sender=Profile)
def invalidate_admin_profile_cache(sender, instance, **kwargs):
    cache.delete(f"admin_profile:{instance.id}")


@receiver([post_save, post_delete], sender=OrderModel)
def invalidate_admin_orders_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_orders:*")
    cache.delete(f"admin_order:{instance.id}")


@receiver([post_save, post_delete], sender=CouponModel)
def invalidate_admin_coupons_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_coupons:*")
    cache.delete(f"admin_coupon:{instance.slug}")


@receiver([post_save, post_delete], sender=PaymentModel)
def invalidate_admin_payments_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_payments:*")
    cache.delete(f"admin_payment:{instance.id}")


@receiver([post_save, post_delete], sender=ProductModel)
def invalidate_admin_products_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_products:*")
    cache.delete(f"admin_product:{instance.slug}")


@receiver([post_save, post_delete], sender=CategoryModel)
def invalidate_admin_categories_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_categories:*")
    cache.delete(f"admin_category:{instance.slug}")


@receiver([post_save, post_delete], sender=TicketModel)
def invalidate_admin_tickets_cache(sender, instance, **kwargs):
    cache.delete_pattern("admin_tickets:*")
    cache.delete(f"admin_ticket:{instance.pk}")




# Customer dashboard cache
@receiver([post_save, post_delete], sender=Profile)
def invalidate_customer_profile_cache(sender, instance, **kwargs):
    cache.delete(f"customer_profile:{instance.id}")


@receiver([post_save, post_delete], sender=OrderModel)
def invalidate_customer_orders_cache(sender, instance, **kwargs):
    cache.delete_pattern(f"customer_orders:{instance.user.id}_*")
    cache.delete(f"customer_order:{instance.user.id}_{instance.id}")