from django.shortcuts import render
from clubs.models import Book, Club, Moment
from django.views.generic.list import ListView
from clubs.forms import MomentForm
from django.contrib.auth.mixins import LoginRequiredMixin
import random, operator
from operator import attrgetter
from ..book_database.N_based_MSD_Item import generate_recommendations


class DashboardView(LoginRequiredMixin, ListView):
    """docstring for DashboardView."""

    http_method_names = ['get']
    template_name = 'dashboard.html'

    def get_follower_moments(self, follower):
        return follower.moment_set.all().order_by('-created_on')[:5]

    def get_recommendations(self):
        user_id = self.request.user.id
        recommendations = generate_recommendations(user_id)
        return recommendations

    def flatten(self, list):
        return [item for sublist in list for item in sublist]

    def get_queryset(self):
        user_moments = list(self.request.user.moment_set.all().order_by('-created_on')[:5])
        follower_moment_list = self.flatten(list(map(self.get_follower_moments, self.request.user.followers.all())))
        flat_moment_list = self.flatten([user_moments, follower_moment_list])
        flat_moment_list.sort(key=operator.attrgetter('created_on'), reverse=True)
        return flat_moment_list

    def get_context_data(self, **kwargs):
        club_list = list(Club.objects.all())
        clubs_range = range(len(club_list))
        clubs_sample = list(random.sample(club_list, len(club_list) if len(club_list) < 4 else 3))
        recommended_books = self.get_recommendations()
        context = super().get_context_data(**kwargs)
        context['form'] = MomentForm()
        context['random_clubs'] = clubs_sample
        context['recommendations'] = recommended_books
        return context
