from web3_auction.auction.models import Auction
from .serializers import AuctionSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated


class AuctionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer

    def get_queryset(self):
        return Auction.objects.all()


auction_api_list_view = AuctionListView.as_view()


class AuctionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer

    def get_queryset(self):
        return Auction.objects.all()


auction_api_detail_view = AuctionDetailView.as_view()
