from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Auction(models.Model):
    """
    Model to represent an auction.

    Attributes:
    - owner: Auction owner (ForeignKey to User)
    - title: Auction title (max length: 100)
    - description: Auction description
    - image: Image associated with the auction (optional)
    - start_price: Starting price of the auction (positive integer, default: 0)
    - end_price: Final price of the auction (positive integer, optional)
    - start_date: Date and time when the auction starts (auto-generated on addition)
    - end_date: Date and time when the auction ends (optional)
    - winner: Auction winner (optional)
    - is_active: Auction's active status (default: True)
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_owner")
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    start_price = models.PositiveIntegerField(default=0)
    end_price = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="auction_winner",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Auction")
        verbose_name_plural = _("Auctions")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Auction_detail", kwargs={"pk": self.pk})


class Bid(models.Model):
    """
    Model to represent a bid.

    Attributes:
    - auction: The auction associated with this bid (ForeignKey to Auction model)
    - bidder: The user who placed the bid (ForeignKey to User)
    - amount: The bid amount (positive integer, default: 0)
    - bid_date: Date and time when the bid is made (auto-generated)
    """

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    bid_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")

    def __str__(self):
        return f"User: {self.bidder.email} | Auction: {self.auction.title} | Bid: {str(self.amount)}"
