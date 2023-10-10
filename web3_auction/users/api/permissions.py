from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):

    def has_object_permission(self, request, obj):
        profile = obj
        return profile.user == request.user


