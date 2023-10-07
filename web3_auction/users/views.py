from django.contrib.auth import get_user_model
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView

User = get_user_model()


class UserListView(ListView):
    context_object_name = "users"
    template_name = "../templates/users/user_list.html"

    def get_queryset(self):
        return User.objects.all()


user_list_view = UserListView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:profile-detail", kwargs={"pk": self.request.user.profile.pk})


user_redirect_view = UserRedirectView.as_view()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "profile"
    template_name = None

    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        profile = self.get_object()
        followers = profile.followers.all()
        following = profile.following.all()

        context['followers'] = followers
        context['following'] = following
        context['is_following'] = user in followers

        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = "../templates/profile/profile_update.html"

    def form_valid(self, form):
        form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_queryset(self):
        return Profile.objects.all()

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

    return redirect('users:profile-detail', pk=profile_id)

