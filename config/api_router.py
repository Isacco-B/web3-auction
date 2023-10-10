from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from web3_auction.users.api.views import (
    profile_api_list_view,
    profile_api_detail_view,
    profile_api_update_view,
    profile_api_delete_view,
)
from web3_auction.auction.api.views import (
    auction_api_list_view,
    auction_api_detail_view,
    auction_api_create_view,
    auction_api_update_view,
    auction_api_delete_view,
)
from web3_auction.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"

urlpatterns = [
    # Auction Url
    path("auctions/", view=auction_api_list_view),
    path("create-auction/", view=auction_api_create_view),
    path("auction/<pk>/", view=auction_api_detail_view),
    path("auction/<pk>/update/", view=auction_api_update_view),
    path("auction/<pk>/delete/", view=auction_api_delete_view),
    # Profile Url
    path("profiles/", view=profile_api_list_view),
    path("profile/<pk>/", view=profile_api_detail_view),
    path("profile/<pk>/update/", view=profile_api_update_view),
    path("profile/<pk>/delete/", view=profile_api_delete_view),
]

urlpatterns += router.urls
