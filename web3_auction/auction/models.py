from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Auction(models.Model):
    """
    Model to represent an auction.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        blank=True, null=True, upload_to="auction/", default="../static/images/auction/default.svg"
    )
    current_price = models.PositiveIntegerField(default=0)
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
    txId = models.CharField(blank=True, null=True, max_length=100)
    status = models.CharField(default="Active", max_length=10)

    class Meta:
        verbose_name = _("Auction")
        verbose_name_plural = _("Auctions")
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("auctions:detail", kwargs={"pk": self.pk})

    def is_favorited_by_user(self, user):
        return self.favorited_by.filter(id=user.profile.id).exists()


class Bid(models.Model):
    """
    Model to represent a bid.
    """

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    bid_date = models.DateTimeField(auto_now_add=False, auto_now=False)

    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")
        ordering = ["-bid_date"]

    def __str__(self):
        return f"User: {self.bidder.email} | Auction: {self.auction.title} | Bid: {str(self.amount)}"
