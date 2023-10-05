from django.forms import ModelForm
from .models import Auction, Bid


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = (
            "title",
            "description",
            "image",
            "start_price",
            "start_price",
        )


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ("amount",)
