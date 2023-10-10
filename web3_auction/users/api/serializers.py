from rest_framework.serializers import ModelSerializer
from web3_auction.users.models import Profile

from django.contrib.auth import get_user_model
from web3_auction.users.models import User as UserType


User = get_user_model()


class UserSerializer(ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "username",
            "description",
            "profile_image",
            "age",
            "gender",
            "city",
            "phone_number",
            "website_url",
            "x_url",
            "instagram_url",
            "tiktok_url",
            "followers",
            "following",
        )
