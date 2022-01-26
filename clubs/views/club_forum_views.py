from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from clubs.models import Club,User,Post
from django.views.generic import ListView
from django.views import View

class ClubForumView(LoginRequiredMixin, ListView):
    """View handle club forum"""
    model = Post
    template_name = "forum.html"
    context_object_name = 'posts'
    paginate_by = settings.POSTS_PER_PAGE
    pk_url_kwarg = 'club_id'

    def get_queryset(self):
        """Return the club's forum."""
        current_user = self.request.user
        club = Club.objects.get(id=club_id)
        authors = list(club.members.all()) + [current_user]
        posts = Post.objects.filter(author__in=authors)
        return posts
