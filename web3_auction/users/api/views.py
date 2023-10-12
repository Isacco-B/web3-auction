from web3_auction.users.models import Profile
from .serializers import ProfileSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated


class ProfileListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


profile_api_list_view = ProfileListView().as_view()


class ProfileDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


profile_api_detail_view = ProfileDetailView().as_view()
