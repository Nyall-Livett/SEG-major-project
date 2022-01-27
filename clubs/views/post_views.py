from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse
from clubs.forms import PostForm
from clubs.models import Post, Club
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class NewPostView(LoginRequiredMixin, CreateView):
    """Class-based generic view for new post handling."""

    model = Post
    template_name = 'forum.html'
    form_class = PostForm
    http_method_names = ['post']

    def form_valid(self, form):
        """Process a valid form."""
        form.instance.author = self.request.user
        form.instance.club = Club.objects.get(id=self.kwargs.get('club_id'))
        if(form.instance.author not in form.instance.club.members.all()):
            raise PermissionDenied()
        messages.add_message(self.request, messages.SUCCESS, f"You have successfully add a new post to forums.")
        return super().form_valid(form)

    def get_success_url(self):
        """Return URL to redirect the user too after valid form handling."""
        return reverse('club_forum', kwargs = {'club_id' : self.kwargs.get('club_id')})

    def handle_no_permission(self):
        return redirect('log_in')
