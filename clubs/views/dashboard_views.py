from django.shortcuts import render
from clubs.models import Book, Club
import random

book_list = list(Book.objects.all())
if (Book.objects.count() >= 3):
    books = random.sample(book_list, 3)
elif(Book.objects.count() >= 2):
    books = random.sample(book_list, 2)
elif(Book.objects.count() >= 1):
    books = random.sample(book_list, 1)
else:
    books = random.sample(book_list, 0)

club_list = list(Club.objects.all())
if (Club.objects.count() >= 3):
    clubs = random.sample(club_list, 3)
elif(Club.objects.count() >= 2):
    clubs = random.sample(club_list, 2)
elif(Club.objects.count() >= 1):
    clubs = random.sample(club_list, 1)
else:
    clubs = random.sample(club_list, 0)

def dashboard(request):
    return render(request, 'dashboard.html', {'books': books, 'clubs': clubs})



# class ClubPageView(LoginRequiredMixin, View):
#     """ View that handles club page. """

#     """Render log in template with blank log in form."""
#     def render(self):
#         self.request.

#         return render(self.request, 'log_in.html', {'form': form, 'next': self.next})
