from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from web3_auction.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Web3 Auction.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = models.EmailField(_("email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(models.Model):
    """
    Custom User Model with Additional Fields

    This custom User model extends the built-in AbstractUser class provided by Django
    to incorporate additional fields specific to our application's user representation.

    """

    # Choices for the 'gender' field
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    # About
    username = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to="profile/", default="../static/images/profile/default.svg")
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50, default="Other")
    city = models.CharField(max_length=50, blank=True)
    # Contact
    phone_number = models.CharField(max_length=12, blank=True)
    website_url = models.URLField(max_length=200, blank=True)
    x_url = models.URLField(max_length=200, blank=True)
    instagram_url = models.URLField(max_length=200, blank=True)
    tiktok_url = models.URLField(max_length=200, blank=True)
    # Follower
    followers = models.ManyToManyField(User, related_name="following", blank=True)
    following = models.ManyToManyField(User, related_name="followers", blank=True)
    # Favorite
    favorite_auctions = models.ManyToManyField("auction.Auction", related_name="favorited_by", blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
