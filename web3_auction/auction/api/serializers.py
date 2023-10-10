from rest_framework.serializers import ModelSerializer
from  web3_auction.auction.models import Auction


class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "image",
            "current_price",
            "end_price",
            "start_date",
            "end_date",
            "winner",
            "is_active"
        )
