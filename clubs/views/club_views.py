from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from clubs.models import Club
from django.contrib import messages

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
        return reverse("home")
