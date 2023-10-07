from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Auction, Bid


User = get_user_model()


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = (
            "title",
            "description",
            "image",
            "current_price",
            "end_date",
        )
        labels = {
            'current_price': 'Initial price'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Your auction title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Your auction description'}),
            'current_price': forms.TextInput(attrs={'placeholder': 'Initial price'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'} )
        }

class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop(
            "request", None
        )
        super(BidForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields = ("amount",)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        user = User.objects.get(email=self.request.user.email)
        pass
        # if order_price > user.usd_balance and order_type == 'Buy':
        #     raise ValidationError('insufficient funds')
        # elif order_price <= 0:
        #     raise ValidationError('enter a number greater than zero')
        # return order_price


