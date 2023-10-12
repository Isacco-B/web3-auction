from django.db.models.signals import post_delete
from .models import Auction
from django.core.cache import cache
from django.dispatch import receiver


@receiver(post_delete, sender=Auction)
def delete_cache(sender, instance, **kwargs):
    try:
        auction_id = instance.id
        cache_key = f"auction_{auction_id}"
        cache.delete(cache_key)
    except Exception as e:
        print(f"An error occurred during post_delete signal: {e}")


