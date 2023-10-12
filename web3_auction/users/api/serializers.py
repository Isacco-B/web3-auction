from rest_framework.serializers import ModelSerializer
from web3_auction.users.models import Profile


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
