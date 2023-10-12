from django.urls import path

from .views import (
    user_redirect_view,
    user_delete_view,
    # Profile
    ProfileDetailView,
    profile_update_view,
    follow_user,
    toggle_favorite_auction,
)

app_name = "users"
urlpatterns = [
    # User
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~delete/<int:pk>/", view=user_delete_view, name="delete"),
    # Profile
    path(
        "~profile/<int:pk>/",
        view=ProfileDetailView.as_view(template_name="../templates/profile/profile_detail.html"),
        name="profile-detail",
    ),
    path("~profile/update/<int:pk>/", view=profile_update_view, name="profile-update"),
    path("~profile/<int:profile_id>/follow/", view=follow_user, name="follow_user"),
    path(
        "~profile/<int:pk>/follower/",
        view=ProfileDetailView.as_view(template_name="../templates/profile/profile_follower.html"),
        name="profile-follower",
    ),
    path(
        "~profile/<int:pk>/following/",
        view=ProfileDetailView.as_view(template_name="../templates/profile/profile_following.html"),
        name="profile-following",
    ),
    path('~profile/favorite/<int:auction_id>/', view=toggle_favorite_auction, name='toggle-favorite-auction'),
]
