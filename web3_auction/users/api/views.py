from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer

from web3_auction.users.models import Profile
from .serializers import ProfileSerializer
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsProfileOwner


User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProfileListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


profile_api_list_view = ProfileListView().as_view()


class ProfileDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


profile_api_detail_view = ProfileDetailView().as_view()


class ProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


profile_api_update_view = ProfileUpdateView().as_view()


class ProfileDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        return Profile.objects.all()


profile_api_delete_view = ProfileDeleteView().as_view()
