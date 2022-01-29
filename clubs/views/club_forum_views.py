from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from clubs.models import Club,User,Post
from django.views.generic import ListView
from django.views import View
from clubs.forms import PostForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class ClubForumView(LoginRequiredMixin, ListView):
    """View handle club forum"""
    model = Post
    template_name = "forum.html"
    context_object_name = 'posts'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        """Return the club's forum."""
        current_user = self.request.user
        club = Club.objects.get(id=self.kwargs.get('club_id'))
        # authors = list(club.members.all()) + [current_user]
        authors = list(club.members.all())
        if(current_user not in club.members.all()):
            raise PermissionDenied()
        posts = Post.objects.filter(author__in=authors, club = club)
        return posts

    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))
        context['form'] = PostForm()
        return context
