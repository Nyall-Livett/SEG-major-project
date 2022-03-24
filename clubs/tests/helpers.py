from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin
from clubs.models import Post
import urllib.request
import fnmatch


def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

def create_posts(author, club, from_count, to_count):
    """Create unique numbered posts for testing purposes."""
    for count in range(from_count, to_count):
        title = f'Post__title{count}'
        body = f'Post__body{count}'
        post = Post(author=author, club = club, body=body, title=title)
        post.save()

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()


class MenuTesterMixin(AssertHTMLMixin):
    menu_urls = [
        reverse('user_list'), reverse('dashboard'), reverse('password'),
        reverse('profile'), reverse('log_out')
    ]

    def assert_menu(self, response):
        for url in self.menu_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_menu(self, response):
        for url in self.menu_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

def isUrlLegit(url):
    if(url == None):
        return False
    url_chk = url.split('/')
    if fnmatch.fnmatch(url_chk[0], 'http*'):
        url = url
    else:
        url = 'http://%s' %(url)

    try:
        response = urllib.request.urlopen(url).read()
        if response:
            return True
    except Exception:
        return False
        
