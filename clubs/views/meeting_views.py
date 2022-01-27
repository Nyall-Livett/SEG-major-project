import random
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from clubs.models import Meeting

from clubs.forms import MeetingForm

"""Temporily stored in club_view, but this should belongs to meeting_views.py"""
from clubs.models import Meeting

from clubs.forms import MeetingForm

def meeting_set(request):
    """Geting clubs, this is an unfinished function because the clubsa and users are not inserted yet"""

    form = MeetingForm(initial = {"member_selected":)

    """member_list = club.member.objects.get()
    size = len(member_list)//2
    random = [random.randint(0, len(member_list)) for i in range(size)]
    String =""
    for i in random:
        string += member_list[i].name +'\n'
    return string"""
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    return render(request,"set_meeting.html", {'form': form})
