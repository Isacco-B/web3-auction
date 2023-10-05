from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuctionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web3_auction.auction"
    verbose_name = _("Auctuons")
