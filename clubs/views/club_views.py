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
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from clubs.forms import MeetingForm
from clubs.forms import BookForm

from clubs.models import Book, Club, Meeting, User, Notification, Post
from clubs.forms import ClubForm
from clubs.factories.notification_factory import CreateNotification
from clubs.enums import NotificationType


#from random import randint


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

class pending_requests(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'pending_requests.html'
    pk_url_kwarg = 'club_id'


    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)



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

    def get(self, request, *args, **kwargs):
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


class PreviousMeetingView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'previous_meetings.html'
    context_object_name = "meetings"
    paginate_by = settings.MEETINGS_PER_PAGE


    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        return context


class CreateMeetingView(LoginRequiredMixin, FormView):
    """docstring for CreateMeetingView."""

    template_name = "set_meeting.html"
    form_class = MeetingForm

    def form_valid(self, form):
        meeting = form.instance
        #schedule = form.save(commit=False)
        #count = User.objects.count()
        #schedule.chosen_member = User.objects.all()[randint(0, count - 1)]
        #schedule.save()
        form.save()
        meeting.add_meeting(self.request.meeting)
        return super().form_valid(form)

    def get(self, request):

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

        return redirect('show_club', club_id = self.club.id)

class rejectMembership(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        super().setup(self, request, user_id, club_id, *args, **kwargs)
        self.club = Club.objects.get(id=club_id)
        self.user = User.objects.get(id=user_id)

    def post(self, request, user_id, club_id, *args, **kwargs ):
        self.club.rejectmembership(self.user)

        return redirect('show_club', club_id = self.club.id)


# """@login_required
# def join_club(request, user_id,club_id):
#     club = Club.objects.get(id=club_id)
#     user = User.objects.get(id=user_id)
#     try:
#         if club.members.count() >= club.maximum_members:
#             messages.add_message(request, messages.WARNING,
#                 f" Cannot join {club.name}. Member capacity has been reached")
#             return redirect('club_list')
#         else:
#             club.add_or_remove_member(user)
#             notifier = CreateNotification()
#             notifier.notify(NotificationType.CLUB_ACCEPTED, request.user, {'club_name': club.name})
#             messages.add_message(request, messages.SUCCESS,
#                 f"You have successfully joined {club.name} ")
#             return redirect('club_list')


#     except ObjectDoesNotExist:
#         return redirect('club_list')
#     else:
#         return redirect('club_list', user_id=user_id)

# @login_required
# def leave_club(request, user_id,club_id):
#     club = Club.objects.get(id=club_id)
#     user = User.objects.get(id=user_id)
#     try:
#         club.add_or_remove_member(user)
#         messages.add_message(request, messages.SUCCESS,
#             f"You have left {club.name} ")
#         return redirect('club_list')
#     except ObjectDoesNotExist:
#     def redirect(self):
#         return redirect('club_list')
