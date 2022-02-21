from django.shortcuts import render
from clubs.models import Book, Club, Moment
from django.views.generic.list import ListView
from clubs.forms import MomentForm
from django.contrib.auth.mixins import LoginRequiredMixin
import random

class DashboardView(LoginRequiredMixin, ListView):
    """docstring for DashboardView."""

    http_method_names = ['get']
    template_name = 'dashboard.html'

    def get_queryset(self):
        user_moments = self.request.user.moment_set.all().order_by('-created_on')
        return user_moments

    def get_context_data(self, **kwargs):
        club_list = list(Club.objects.all())
        clubs_range = range(len(club_list))
        self.clubs_sample = list(random.sample(club_list, len(club_list) if len(club_list) < 7 else 6))
        context = super().get_context_data(**kwargs)
        context['form'] = MomentForm()
        context['random_clubs'] = self.clubs_sample
        return context
