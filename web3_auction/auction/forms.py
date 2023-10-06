from django.forms import ModelForm
from .models import Auction, Bid


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = (
            "title",
            "description",
            "image",
            "current_price",
        )
        labels = {
            'current_price': 'Price'
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ("amount",)
