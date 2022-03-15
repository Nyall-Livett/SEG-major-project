"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views
from clubs.forms import BookAutocomplete



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('delete_account/<int:user_id>', views.DeleteAccount.as_view(), name='delete_account'),
    path('delete_club/<int:club_id>', views.DeleteClub.as_view(), name='delete_club'),
    path('follow_requests/', views.FollowRequestsListView.as_view(), name='follow_requests_page'),
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('club/<int:club_id>',views.ShowClubView.as_view(), name ='show_club'),
    path('follow_toggle/<int:user_id>',views.follow_toggle, name ='follow_toggle'),
    path('follow_request/<int:user_id>',views.follow_request, name ='follow_request'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('set_meeting/<int:club_id>', views.CreateMeetingView.as_view(), name='set_meeting'),
    path('start_meeting/<slug:pk>/', views.StartMeetingView.as_view(), name='start_meeting'),
    path('edit_meeting/<slug:pk>/', views.EditMeetingView.as_view(), name='edit_meeting'),
    path('book/', views.CreateBookView.as_view(), name='book'),
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    path('join_club/<int:user_id><int:club_id>', views.JoinRemoveClubView.as_view(), name='join_club'),
    path('acceptMembership/<int:user_id><int:club_id>', views.acceptClubapplication.as_view() ,name = 'acceptMembership'),
    path('rejectMembership/<int:user_id><int:club_id>', views.rejectMembership.as_view() ,name = 'rejectMembership'),
    path('create_club/', views.CreateClubView.as_view(), name='create_club'),
    path('create_moment/', views.CreateMomentView.as_view(), name='create_moment'),
    path('transfer_ownership/', views.TransferClubLeadership.as_view(), name='transfer_ownership'),
    path('forum/<int:club_id>', views.ClubForumView.as_view(), name='club_forum'),
    path('new_post/<int:club_id>', views.NewPostView.as_view(), name='new_post'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('upload_books/', views.UploadBooksView.as_view(), name='upload_books'),
    path('book/<int:book_id>',views.ShowBookView.as_view(), name ='show_book'),
    path('book_review', views.BookReviewView.as_view(), name='book_review'),
    path('accept_request/<int:user_id>', views.accept_request, name='accept_request'),
    path('reject_request/<int:user_id>', views.reject_request, name='reject_request'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('pending_requests/<int:club_id>', views.pending_requests.as_view(), name = 'pending_requests'),
    path('show_followers/<int:user_id>', views.FollowersListView.as_view(), name='show_followers'),
    path('show_following/<int:user_id>', views.FollowingListView.as_view(), name='show_following'),
    path('notification_mark_all_acted_upon/', views.NotificationMarkAllActedUpon.as_view(), name='notification_mark_all_acted_upon'),
    path('notification_mark_all_not_acted_upon/', views.NotificationMarkAllNotActedUpon.as_view(), name='notification_mark_all_not_acted_upon'),
    path('notification_delete/', views.NotificationDelete.as_view(), name='notification_delete'),
    path('previous_meetings/<int:club_id>', views.PreviousMeetingView.as_view(), name= 'previous_meetings'),
    path('member_list/<int:club_id>', views.MemberListView.as_view(), name='member_list'),
    path('change_theme/<int:club_id>', views.ChangeClubTheme.as_view(), name='change_theme'),
    path('book-autocomplete', BookAutocomplete.as_view(), name='book-autocomplete'),
]
