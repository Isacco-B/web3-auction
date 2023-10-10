from django.core.exceptions import PermissionDenied


class IsAuctionOwner:
    def dispatch(self, request, *args, **kwargs):
        auction = self.get_object()
        if auction.owner.profile.id != request.user.profile.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

