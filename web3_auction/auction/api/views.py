from web3_auction.auction.models import Auction
from .serializers import AuctionSerializer
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuctionOwner


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


class AuctionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


auction_api_create_view = AuctionCreateView.as_view()


class AuctionUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuctionOwner]
    serializer_class = AuctionSerializer

    def get_queryset(self):
        return Auction.objects.filter(is_aviable=True)


auction_api_update_view = AuctionUpdateView.as_view()


class AuctionDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuctionOwner]

    def get_queryset(self):
        return Auction.objects.all()


auction_api_delete_view = AuctionDeleteView.as_view()
