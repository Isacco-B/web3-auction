import json
from celery import shared_task
from django.core.cache import cache
from .models import Bid

@shared_task
def move_bids_from_cache_to_db(auction_id):
    cache_keys = cache.keys(f'bid:*:auction_id:{auction_id}')
    for cache_key in cache_keys:
        bid_data = json.loads(cache.get(cache_key))

        bid = Bid.objects.create(
            id=bid_data['id'],
            amount=bid_data['amount'],
            bidder_id=bid_data['bidder_id'],
            auction_id=bid_data['auction_id']
        )
        bid.save()

        cache.delete(cache_key)
