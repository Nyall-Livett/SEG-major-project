"""Club related views."""
import random
from django.conf import settings
from django.views.generic.edit import FormView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.http import JsonResponse
from django.db import IntegrityError
import json
import random
from clubs.models import Book, Club, User, Notification, Post
from clubs.forms import ClubForm, MeetingForm
from clubs.factories.notification_factory import CreateNotification
from clubs.factories.moment_factory import CreateMoment
from clubs.enums import NotificationType, MomentType

from clubs.zoom_api_url_generator_helper import getZoomMeetingURLAndPasscode, create_JSON_meeting_data, convertDateTime, getZoomMeetingURLAndPasscode


class CreateClubView(LoginRequiredMixin, FormView):
    """docstring for CreateClubView."""

    template_name = "create_club.html"
    form_class = ClubForm

    def form_valid(self, form):
        club = form.instance
        club.leader = self.request.user
        club.save()
        club.add_or_remove_member(self.request.user)
        notifier = CreateNotification()
        notifier.notify(NotificationType.CLUB_CREATED, self.request.user, {'club': club})
        messages.add_message(self.request, messages.SUCCESS, f"You have successfully created {club.name}.")
        moment_notifier = CreateMoment()
        moment_notifier.notify(MomentType.CLUB_CREATED, self.request.user, {'club': club})
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("club_list")

class TransferClubLeadership(LoginRequiredMixin, View):
    """docstring for TransferClubLeadership."""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            club_id = json.loads(request.POST.get('club_id'))
            new_leader_id = json.loads(request.POST.get('new_leader_id'))
            club = Club.objects.get(id=club_id)
            new_leader = User.objects.get(id=new_leader_id)

            if (request.user == club.leader and new_leader in club.members.all()):
                club.leader = new_leader
                club.save()
                notifier = CreateNotification()
                notifier.notify(NotificationType.CLUB_RECEIVED, new_leader, {'club': club})
                messages.add_message(self.request, messages.SUCCESS, f"You have successfully transferred leadership of {club.name}.")
                return JsonResponse({
                    'redirect_url': reverse('show_club', args=[club_id])
                }, status=200)
            raise PermissionDenied()


class pending_requests(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'pending_requests.html'
    pk_url_kwarg = 'club_id'


    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        return context

class ShowClubView(LoginRequiredMixin, DetailView):

    model = Club
    template_name = 'show_club.html'
    pk_url_kwarg = 'club_id'

    def get(self, request, club_id, optional_notification="", *args, **kwargs):
        if optional_notification:
            notification = Notification.objects.get(id=optional_notification)
            if notification.receiver == request.user and notification.acted_upon == False:
                notification.acted_upon = True
                notification.save()

        """Handle get request, and redirect to club_list if club_id invalid."""
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('club_list')

    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        authors = list(context['club'].members.all())
        context['posts'] = Post.objects.filter(author__in=authors, club = context['club'])[:20]
        return context


class ClubListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = Club
    template_name = "club_list.html"
    context_object_name = "clubs"
    paginate_by = settings.USERS_PER_PAGE

class JoinRemoveClubView(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        super().setup(self, request, user_id, club_id, *args, **kwargs)
        self.club = Club.objects.get(id=club_id)
        self.user = User.objects.get(id=user_id)

    def post(self, request, user_id, club_id, *args, **kwargs ):
        if self.user in self.club.members.all():
            if self.user.id is self.club.leader.id:
                messages.add_message(request, messages.WARNING,
                    f" Club leader cannot leave club ")
            else:
                self.club.add_or_remove_member(self.user)
                messages.add_message(request, messages.WARNING,
                    f"You have left {self.club.name} ")
        else:
            if self.club.members.count() >= self.club.maximum_members:
                messages.add_message(request, messages.WARNING,
                    f" Cannot join {self.club.name}. Member capacity has been reached")
            else:
                self.club.applicant_manager(self.user)
                messages.add_message(request, messages.SUCCESS,
                    f"You have applied to join {self.club.name} ")
        return redirect('club_list')


class acceptClubapplication(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        super().setup(self, request, user_id, club_id, *args, **kwargs)
        self.club = Club.objects.get(id=club_id)
        self.user = User.objects.get(id=user_id)

    def post(self, request, user_id, club_id, *args, **kwargs ):
        self.club.acceptmembership(self.user)
        notifier = CreateNotification()
        notifier.notify(NotificationType.CLUB_JOINED, self.user, {'club': self.club})
        return redirect('pending_requests', club_id = self.club.id)

class rejectMembership(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        super().setup(self, request, user_id, club_id, *args, **kwargs)
        self.club = Club.objects.get(id=club_id)
        self.user = User.objects.get(id=user_id)

    def post(self, request, user_id, club_id, *args, **kwargs ):
        self.club.rejectmembership(self.user)

        return redirect('pending_requests', club_id = self.club.id)

class ChangeClubTheme(LoginRequiredMixin, UpdateView):
    model = Club
    fields = ['theme']
    template_name = 'change_theme.html'
    pk_url_kwarg = 'club_id'

    def get_context_data(self, **kwargs):
        """Return context data"""

        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        return context

    def get_success_url(self):
        self.club = Club.objects.get(id=self.kwargs.get('club_id'))
        self.user = self.request.user
        club_leader = self.club.leader.id
        """Return URL to redirect the user too after valid form handling."""
        if self.user.id is club_leader:
            return reverse('show_club', kwargs = {'club_id' : self.kwargs.get('club_id')})
        else:
            raise Http404("Object you are looking for doesn't exist")


class DeleteClub(LoginRequiredMixin, DeleteView):
    """View that allows a user to delete their club"""

    model = Club
    template_name = "delete_club.html"
    pk_url_kwarg = 'club_id'

    def get_context_data(self, **kwargs):
        """Return context data"""

        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        return context

    def delete(self, request, *args, **kwargs):

        self.club = Club.objects.get(id=self.kwargs.get('club_id'))
        self.user = request.user
        club_leader = self.club.leader.id

        if self.user.id is club_leader:

            return super(DeleteClub, self).delete(request, *args, **kwargs)
        else:
            raise Http404("Object you are looking for doesn't exist")

    def get_success_url(self):
        # self.delete_account_url =  f'/delete_account/{self.user.id}'
        return reverse('club_list')

