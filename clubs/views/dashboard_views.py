from clubs.models import Book, Club
from django.views.generic.list import ListView
from clubs.forms import MomentForm
from django.contrib.auth.mixins import LoginRequiredMixin
import random, operator
from ..helpers import generate_ratings,contain_ratings
from ..N_based_RecSys_Algorithm.N_based_MSD_Item import generate_recommendations
from django.db.models import Count


class DashboardView(LoginRequiredMixin, ListView):
    """docstring for DashboardView."""

    http_method_names = ['get']
    template_name = 'dashboard.html'

    def get_follower_moments(self, follower):
        return follower.moment_set.all().order_by('-created_on')[:5]

    def get_recommendations(self):
        user_id = self.request.user.id
        if(Book.objects.count() > 0):
            if((contain_ratings(user_id))==False):
                book = Book.objects.all().first()
                generate_ratings(book,user_id,'neutral')
            recommendations = generate_recommendations(user_id)
            return recommendations
        else:
            return None

    def get_popular_clubs(self):
        if Club.objects.count() < 4:
            return Club.objects.all()

        ordered_clubs = list(Club.objects.annotate(member_count=Count('members')).order_by('-member_count'))
        bias = int(len(ordered_clubs) / 5)
        selected = set()
        counter = 0
        while len(selected) < 3:
            if counter >= 15:
                selected = random.sample(ordered_clubs, 3)
                break
            id = int(random.triangular(0, len(ordered_clubs), 1))
            selected.add(ordered_clubs[id])
            counter = counter + 1
        return selected

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
        recommended_books = self.get_recommendations()
        context = super().get_context_data(**kwargs)
        context['form'] = MomentForm()
        context['random_clubs'] = self.get_popular_clubs()
        context['recommendations'] = recommended_books
        return context
