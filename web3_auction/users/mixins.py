from django.core.exceptions import PermissionDenied


class IsProfileOwner:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.id != request.user.profile.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class IsUserOwner:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.id != request.user.profile.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
