import json
from celery import shared_task
from django.core.cache import cache
from .models import Bid, Auction
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


def move_bids_from_cache_to_db(auction_id):
    cache_key = f"auction_{auction_id}"
    existing_bid_data = json.loads(cache.get(cache_key))
    for bid_data in existing_bid_data:
        auction = Auction.objects.get(pk=auction_id)
        user_id = int(bid_data["user_id"])
        bidder_user = User.objects.get(pk=user_id)
        amount = int(bid_data["amount"])

        bid = Bid.objects.create(
            auction=auction,
            bidder=bidder_user,
            amount=amount,
            bid_date=bid_data["bid_date"],
        )
        bid.save()

    cache.delete(cache_key)


@shared_task
def close_auctions():
    current_datetime = timezone.now()
    auctions_to_close = Auction.objects.filter(end_date__lte=current_datetime, is_active=True)

    for auction in auctions_to_close:
        auction.is_active = False

        cache_key = f"auction_{auction.id}"
        existing_bid_data = cache.get(cache_key)

        if existing_bid_data:
            bid_data = json.loads(existing_bid_data)
            last_bid = bid_data[-1]
            user_id = int(last_bid["user_id"])
            winner_user = User.objects.get(pk=user_id)

            auction.end_price = int(last_bid["amount"])
            auction.winner = winner_user

            move_bids_from_cache_to_db(auction.id)

        auction.save()
