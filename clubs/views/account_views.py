"""Account related views."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse
from clubs.forms import PasswordForm, UserForm, SignUpForm
from .mixins import LoginProhibitedMixin
from clubs.models import User, Club, CustomAvatar
from clubs.enums import AvatarIcon, AvatarColor
import random
from ..helpers import generate_favourite_ratings,delete_ratings,generate_a_random_book

class PasswordView(LoginRequiredMixin, FormView):
    """View that handles password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        user = self.get_object()
        generate_favourite_ratings(user.favourite_book,user.id)
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avatar_icons'] = AvatarIcon.values
        context['avatar_colors'] = AvatarColor.values
        return context

    def form_valid(self, form):
        object = form.save()
        avatar = CustomAvatar.objects.get(user=object)
        # Create avatar
        color = self.request.POST['color']
        icon = self.request.POST['icon']

        if color != avatar.color or icon != avatar.icon:
            avatar.color=color
            avatar.icon=icon
            avatar.save()

        return super().form_valid(form)

class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        object = form.save()
        # Create avatar
        color = self.request.POST['color']
        if len(color) < 1:
            color = AvatarColor.values[random.randint(0, len(AvatarColor.values))]
        icon = self.request.POST['icon']
        if len(icon) < 1:
            icon = AvatarIcon.values[random.randint(0, len(AvatarIcon.values))]
        CustomAvatar.objects.create(color=color, icon=icon, user=object)
        login(self.request, object)
        if (object.favourite_book == None):
            # object.favourite_book = generate_a_random_book()
            object.favourite_book = Book.objects.get(id=1)
        generate_favourite_ratings(object.favourite_book,object.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avatar_icons'] = AvatarIcon.values
        context['avatar_colors'] = AvatarColor.values
        return context

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class DeleteAccount(LoginRequiredMixin, DeleteView):
    """View that allows a user to delete their account"""

    model = User
    template_name = "delete_account.html"
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        """Return context data"""

        context = super().get_context_data(**kwargs)
        user = User.objects.get(id= self.kwargs.get('user_id'))
        context['club_list'] = Club.objects.filter(leader=user)
        delete_ratings(user.id)
        return context

    def get_success_url(self):
        return reverse('sign_up')
