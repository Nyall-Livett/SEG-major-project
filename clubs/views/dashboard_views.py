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
        user_moments = self.request.user.moment_set.all()
        return user_moments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MomentForm()
        return context
