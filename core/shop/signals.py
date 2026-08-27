from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ProductModel

@receiver([post_save, post_delete], sender=ProductModel)
def product_list_cache(sender, **kwargs):
    cache.delete_pattern("*product_list*")
