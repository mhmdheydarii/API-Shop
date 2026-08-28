from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ProductModel

@receiver([post_save, post_delete], sender=ProductModel)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete_pattern("product_list:*")
    cache.delete(f"product_detail:{instance.slug}")
    cache.delete("recent_products")
    cache.delete("discounted_products")