from django.urls import path

from .views import (
    auction_create_view,
    auction_list_view,
    auction_detail_view,
    auction_update_view,
    auction_delete_view,
    # Bid
    save_form_data_to_cache,
)


app_name = "auctions"
urlpatterns = [
    path("~create/", view=auction_create_view, name="create"),
    path("~list/", view=auction_list_view, name="list"),
    path("<int:pk>/", view=auction_detail_view, name="detail"),
    path("~update/<int:pk>/", view=auction_update_view, name="update"),
    path("~delete/<int:pk>/", view=auction_delete_view, name="delete"),
    # Bid
    path("~bid/create/<int:pk>/", view=save_form_data_to_cache, name="bid-create"),
]
