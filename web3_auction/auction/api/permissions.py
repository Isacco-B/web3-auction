from rest_framework.permissions import BasePermission


class IsAuctionOwner(BasePermission):

    def has_object_permission(self, request, obj):
        auction = obj
        return auction.owner == request.user


