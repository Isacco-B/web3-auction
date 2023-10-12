from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from web3_auction.users.api.views import (
    profile_api_list_view,
    profile_api_detail_view,
)
from web3_auction.auction.api.views import (
    auction_api_list_view,
    auction_api_detail_view,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


app_name = "api"

urlpatterns = [
    # Auction Url
    path("auctions/", view=auction_api_list_view),
    path("auction/<pk>/", view=auction_api_detail_view),
    # Profile Url
    path("profiles/", view=profile_api_list_view),
    path("profile/<pk>/", view=profile_api_detail_view),
]

urlpatterns += router.urls
