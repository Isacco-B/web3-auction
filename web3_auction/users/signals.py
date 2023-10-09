from django.db.models.signals import post_save
from .models import User, Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_email = instance.email
        username = user_email.split("@")[0]
        Profile.objects.create(user=instance, username=username)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
