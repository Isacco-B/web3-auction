from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from django.core.cache import cache
import json


User = get_user_model()


# -------Auction View-------


class AuctionListView(ListView):
    context_object_name = "auctions"
    template_name = "../templates/auction/auction_list.html"

    def get_queryset(self):
        return Auction.objects.all()


auction_list_view = AuctionListView.as_view()


class AuctionDetailView(DetailView):
    context_object_name = "auction"
    template_name = "../templates/auction/auction_detail.html"

    def get_queryset(self):
        return Auction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bid_form"] = BidForm()
        return context


auction_detail_view = AuctionDetailView.as_view()


class AuctionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AuctionForm
    template_name = "../templates/auction/auction_create.html"
    success_message = "Auction successfully created"

    def form_valid(self, form):
        user = User.objects.get(email=self.request.user.email)
        auction = form.save(commit=False)
        auction.owner = user
        auction.save()
        return super(AuctionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("auctions:list")


auction_create_view = AuctionCreateView.as_view()


class AuctionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    context_object_name = "auction"
    template_name = "../templates/auction/auction_delete.html"
    success_message = "Auction successfully deleted"

    def get_queryset(self):
        return Auction.objects.filter(is_active=True, user=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy("home")


auction_delete_view = AuctionDeleteView.as_view()


# -------Bid View-------


class BidListView(LoginRequiredMixin, ListView):
    context_object_name = "bids"
    template_name = "../templates/bid/bid_list.html"

    def get_queryset(self):
        return Auction.objects.filter(bidder=self.request.user.pk)


bid_list_view = BidListView.as_view()


class BidCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = BidForm
    template_name = "../templates/bid/bid_create.html"
    success_message = "Bid added successfully"

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        auction_id = self.kwargs["pk"]
        auction = get_object_or_404(Auction, pk=auction_id)
        bid = form.save(commit=False)
        bid.bidder = user
        bid.auction = auction

        bid_data = {
            'id': bid.id,
            'amount': bid.amount,
            'bidder_id': bid.bidder.id,
            'auction_id': bid.auction.id
        }

        # Memorizza il bid in cache (utilizza un chiave univoca, ad esempio bid:id)
        cache_key = f'bid:{bid.id}'
        cache.set(cache_key, json.dumps(bid_data), timeout=None)  # timeout=None significa che non scade

        return super(BidCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BidCreateView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse_lazy("auctions:detail", kwargs={"pk": self.kwargs["pk"]})


bid_create_view = BidCreateView.as_view()


class BidDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = "bid"
    template_name = "../templates/bid/bid_delete.html"
    success_message = "Bid successfully deleted"

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy("landing-page")


bid_delete_view = BidDeleteView.as_view()
