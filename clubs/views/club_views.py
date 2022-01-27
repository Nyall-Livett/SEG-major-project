from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from clubs.models import Club, User



from clubs.forms import ClubForm


class CreateClubView(LoginRequiredMixin, FormView):
    """docstring for CreateClubView."""

    template_name = "create_club.html"
    form_class = ClubForm

    def form_valid(self, form):
        club = form.instance
        club.founder = self.request.user
        club.save()
        club.add_member(self.request.user)
        messages.add_message(self.request, messages.SUCCESS, f"You have successfully created {club.name}.")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("dashboard")

class TransferClubOwnership(LoginRequiredMixin, View):
    """docstring for TransferClubOwnership."""
    http_method_names = ['post']

    def setup(self, request, user_id, club_id, *args, **kwargs):
        self.new_owner = User.objects.get(pk=user_id)
        self.club = Club.objects.get(pk=club_id)
        super().setup(request, user_id, club_id, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.id is self.club.founder.id:
            self.club.grant_ownership(self.new_owner)
            messages.add_message(self.request, messages.SUCCESS,
                f"You have successfully passed ownership of {self.club.name} to {self.new_owner.full_name()}.")

            return self.redirect()
        raise PermissionDenied()

    def redirect(self):
        return redirect("dashboard")


"""Temporily stored in club_view, but this should belongs to meeting_views.py"""
from clubs.models import Meeting

from clubs.forms import MeetingForm

def select_member():
    """Geting clubs, this is an unfinished function because the clubsa and users are not inserted yet"""

    member_list = club.members.objects.get()
    size = len(member_list)//2
    random = [random.randint(0, len(member_list)) for i in range(size)]
    String =""
    for i in random:
        string += member_list[i].name +'\n'
    return string

"""def meeting_set(request):

    form = MeetingForm(initial = {"member_selected": "Tom"})

    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    context = {
        'form': form
    }
    return render(request,"set_meeting.html", context)"""
class CreateMeetingView(LoginRequiredMixin, FormView):
    """docstring for CreateClubView."""

    template_name = "set_meeting.html"
    form_class = MeetingForm

    def form_valid(self, form):
        meeting = form.instance
        form.save()
        meeting.add_member(self.request.meeting)
        return super().form_valid(form)

    def get(self, request):
        form = MeetingForm(initial = {"member_selected": "Tom"})
        context = {
            'form': form
        }
        return render(request,"set_meeting.html", context)

    def post(self, request):
        form = MeetingForm(request.POST)
        #form.save()
        if form.is_valid():
            return redirect("dashboard")
        context = {
            'form': form
        }
        #message.add_message(request, messages.ERROR, "This is invaild!")
        return render(request,"set_meeting.html", context)


    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("dashboard")
