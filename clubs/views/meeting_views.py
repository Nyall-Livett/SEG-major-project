"""Meeting related views."""
from re import template
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
from clubs.models import User, Club, Meeting, Book
from clubs.forms import ClubForm, BookForm, MeetingForm, StartMeetingForm, EditMeetingForm, BookReviewForm
from clubs.zoom_api_url_generator_helper import getZoomMeetingURLAndPasscode, create_JSON_meeting_data, convertDateTime, getZoomMeetingURLAndPasscode
import json
import random
from ..helpers import generate_ratings,contain_ratings
from ..N_based_RecSys_Algorithm.N_based_MSD_Item import generate_recommendations

class StartMeetingView(LoginRequiredMixin, UpdateView):
    model = Meeting #model
    form_class = StartMeetingForm
    template_name = 'start_meeting.html' # templete for updating
    success_url="/dashboard" # posts list url

    def get_recommendations(self):
        user_id = self.request.user.id
        if(Book.objects.count() > 0):
            if((contain_ratings(user_id))==False):
                # book = Book.objects.get(id=1)
                book = Book.objects.all().first()
                generate_ratings(book,user_id,'neutral')
            recommendations = generate_recommendations(user_id)
            return recommendations
        else:
            return None

    def get_context_data(self, **kwargs):
        recommended_books = self.get_recommendations()
        context = super().get_context_data(**kwargs)
        context['recommendations'] = recommended_books
        return context

class EditMeetingView(LoginRequiredMixin, UpdateView):
    model = Meeting #model
    form_class = EditMeetingForm
    template_name = 'edit_meeting.html' # templete for updating
    success_url="/dashboard" # posts list url

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
    http_method_names = ['get', 'post']
    template_name = "set_meeting.html"
    pk_url_kwarg = 'club_id'
    form_class = MeetingForm

    def get(self, request, **kwargs):
        form = MeetingForm()
        context = {
            'form': form,
            'club': Club.objects.get(id=self.kwargs.get('club_id'))
        }
        return render(request,"set_meeting.html", context)


    def post(self, request, **kwargs):
        form = MeetingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)


            # Set club, URL and chosen member before save
            obj.club = Club.objects.get(id=self.kwargs.get('club_id'))

            # get meeting title, start time, meeting description and generate a zoom meeting URL
            title = obj.club.name
            start_time = convertDateTime(form.cleaned_data['date'])
            meet_desc = form.cleaned_data['notes']
            json_data = create_JSON_meeting_data(title, start_time, meet_desc)
            meet_url_pass = getZoomMeetingURLAndPasscode(json_data)
            obj.URL = meet_url_pass[0]
            obj.passcode = meet_url_pass[1]

            list = []
            for i in Club.objects.get(id=self.kwargs.get('club_id')).members.all():
                list.append(i)
            obj.chosen_member = random.choice(list)
            obj.save()
            return redirect('show_club', self.kwargs.get('club_id'))

        else:
            context = {
                'form': form,
                'club': Club.objects.get(id=self.kwargs.get('club_id'))
            }

        return render(request,"set_meeting.html", context)
