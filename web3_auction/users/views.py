from django.contrib.auth import get_user_model
from .models import Profile
from web3_auction.auction.models import Auction
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import IsProfileOwner, IsUserOwner
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, DeleteView


User = get_user_model()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:profile-detail", kwargs={"pk": self.request.user.profile.pk})


user_redirect_view = UserRedirectView.as_view()


class UserDeleteView(LoginRequiredMixin, IsUserOwner, DeleteView):
    template_name = "users/user_delete.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse("home")


user_delete_view = UserDeleteView.as_view()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "profile"
    template_name = None

    def get_queryset(self):
        return Profile.objects.all()


class ProfileUpdateView(LoginRequiredMixin, IsProfileOwner, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = "../templates/profile/profile_update.html"

    def form_valid(self, form):
        form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("users:redirect")


profile_update_view = ProfileUpdateView.as_view()


@login_required
def follow_user(request, profile_id):
    profile_to_follow = get_object_or_404(Profile, id=profile_id)
    profile = get_object_or_404(Profile, id=request.user.profile.id)
    user = request.user

    if user != profile_to_follow.user:
        if user in profile_to_follow.followers.all():
            profile_to_follow.followers.remove(user)
            profile.following.remove(profile_to_follow.user)
        else:
            profile_to_follow.followers.add(user)
            profile.following.add(profile_to_follow.user)

    return redirect("users:profile-detail", pk=profile_id)


@login_required
def toggle_favorite_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if auction in request.user.profile.favorite_auctions.all():
        request.user.profile.favorite_auctions.remove(auction)
    else:
        request.user.profile.favorite_auctions.add(auction)

    return redirect("auctions:list")
