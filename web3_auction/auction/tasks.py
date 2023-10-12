import json
from celery import shared_task
from django.core.cache import cache
from .models import Bid, Auction
from django.contrib.auth import get_user_model
from django.utils import timezone

import json
import hashlib
from web3_auction.utils.transaction import sendTransaction


User = get_user_model()


def move_bids_from_cache_to_db(auction_id):
    try:
        cache_key = f"auction_{auction_id}"
        existing_bid_data = json.loads(cache.get(cache_key))
        auction = Auction.objects.get(pk=auction_id)

        for bid_data in existing_bid_data:
            user_id = int(bid_data["user_id"])

            try:
                bidder_user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist.")

            amount = int(bid_data["amount"])
            date = bid_data["bid_date"]

            bid = Bid.objects.create(auction=auction, bidder=bidder_user, amount=amount, bid_date=date)
            bid.save()

        cache.delete(cache_key)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@shared_task
def close_auctions():
    try:
        current_datetime = timezone.now()
        auctions_to_close = Auction.objects.filter(end_date__lte=current_datetime, status="Active")

        for auction in auctions_to_close:
            cache_key = f"auction_{auction.id}"
            existing_bid_data = cache.get(cache_key)

            if existing_bid_data:
                bid_data = json.loads(existing_bid_data)
                last_bid = bid_data[-1]
                user_id = int(last_bid["user_id"])

                try:
                    winner_user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    print(f"User with ID {user_id} does not exist.")

                auction.end_price = int(last_bid["amount"])
                auction.winner = winner_user
                auction.status = "Closed"
                auction.save()

                move_bids_from_cache_to_db(auction.id)
            else:
                auction.status = "Inactive"
                auction.save()
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@shared_task
def send_transaction():
    try:
        auctions_to_send = Auction.objects.filter(status="Closed", txId=None)
        for auction in auctions_to_send:
            auction_details = {
                "id": auction.id,
                "title": auction.title,
                "description": auction.description,
                "current_price": auction.current_price,
                "end_price": auction.end_price,
                "start_date": str(auction.start_date),
                "end_date": str(auction.end_date),
                "winner": auction.winner.id,
            }
            hash_auction_details = hashlib.sha256(json.dumps(auction_details).encode("utf-8")).hexdigest()
            txId = sendTransaction(hash_auction_details)
            auction.txId = txId
            auction.save()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
