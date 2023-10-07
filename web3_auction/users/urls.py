from django.urls import path

from .views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_list_view,
    # Profile
    ProfileDetailView,
    profile_update_view,
    follow_user,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~list/", view=user_list_view, name="user-list"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    # Profile
    path("~profile/<int:pk>/", view=ProfileDetailView.as_view(template_name='../templates/profile/profile_detail.html'), name="profile-detail"),
    path("~profile/update/<int:pk>/", view=profile_update_view, name="profile-update"),
    path('~profile/<int:profile_id>/follow/', view=follow_user, name='follow_user'),
    path('~profile/<int:pk>/follower/', view=ProfileDetailView.as_view(template_name='../templates/profile/profile_follower.html'), name='profile-follower'),
    path('~profile/<int:pk>/following/', view=ProfileDetailView.as_view(template_name='../templates/profile/profile_following.html'), name='profile-following'),

]
