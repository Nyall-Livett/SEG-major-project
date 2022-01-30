from re import template
from django.conf import settings
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from clubs.models import Club, User, Notification
from clubs.forms import ClubForm
from clubs.factories.notification_factory import CreateNotification, NotificationType


class CreateClubView(LoginRequiredMixin, FormView):
    """docstring for CreateClubView."""

    template_name = "create_club.html"
    form_class = ClubForm

    def form_valid(self, form):
        club = form.instance
        club.leader = self.request.user
        club.save()
        club.add_member(self.request.user)
        notifier = CreateNotification()
        notifier.notify(NotificationType.CLUB_CREATED, self.request.user, {'club_name': club.name})
        messages.add_message(self.request, messages.SUCCESS, f"You have successfully created {club.name}.")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("dashboard")

class TransferClubLeadership(LoginRequiredMixin, View):
    """docstring for TransferClubLeadership."""
    http_method_names = ['post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        self.new_owner = User.objects.get(pk=user_id)
        self.club = Club.objects.get(pk=club_id)
        super().setup(request, user_id, club_id, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.id is self.club.leader.id:
            self.club.grant_leadership(self.new_owner)
            messages.add_message(self.request, messages.SUCCESS,
                f"You have successfully passed leadership of {self.club.name} to {self.new_owner.full_name()}.")

            return self.redirect()
        raise PermissionDenied()

    def redirect(self):
        return redirect("dashboard")

class ShowClubView(LoginRequiredMixin, DetailView):

    model = Club
    template_name = 'show_club.html'
    pk_url_kwarg = 'club_id'

    def get(self, request, *args, **kwargs):
        """Handle get request, and redirect to club_list if club_id invalid."""

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('club_list')


class ClubListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = Club
    template_name = "club_list.html"
    context_object_name = "clubs"
    paginate_by = settings.USERS_PER_PAGE

"""Temporily stored in club_view, but this should belongs to meeting_views.py"""
from clubs.models import Meeting

from clubs.forms import MeetingForm


class CreateMeetingView(LoginRequiredMixin, FormView):
    """docstring for CreateMeetingView."""

    template_name = "set_meeting.html"
    form_class = MeetingForm

    def form_valid(self, form):
        meeting = form.instance
        form.save()
        meeting.add_meeting(self.request.meeting)
        return super().form_valid(form)

    def get(self, request):
        """user = User.objects.get(username = request.user)
        clubs = Club.objects.all()

        #c = None
        club_name = ""
        for c in clubs:
            if c.leader == user.username:
                club_name = c.name"""

        #function was created for select random_members but somehow doesn't work
        """size = len(member_list)//2
        random = [random.randint(0, len(member_list)) for i in range(size)]
        random_members =""
        for i in random:
            random_members += member_list[i].name +'\n'
        return random_members"""


        form = MeetingForm()
        context = {
            'form': form
        }
        return render(request,"set_meeting.html", context)


    def post(self, request):
        form = MeetingForm(request.POST)
        form.save()
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            print(form.errors)
        context = {
            'form': form
        }
        #message.add_message(request, messages.ERROR, "This is invaild!")
        return render(request,"set_meeting.html", context)
