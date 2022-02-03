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



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('follow_requests/', views.FollowRequestsListView.as_view(), name='follow_requests_page'),
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('club/<int:club_id>',views.ShowClubView.as_view(), name ='show_club'),
    path('follow_toggle/<int:user_id>',views.follow_toggle, name ='follow_toggle'),
    path('follow_request/<int:user_id>',views.follow_request, name ='follow_request'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('set_meeting/', views.CreateMeetingView.as_view(), name='set_meeting'),
    path('book/', views.CreateBookView.as_view(), name='book'),
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    #path('join_club/<int:user_id><int:club_id>', views.join_club, name='join_club'),
    path('join_club/<int:user_id><int:club_id>', views.JoinRemoveClubView.as_view(), name='join_club'),
    #path('leave_club/<int:user_id><int:club_id>', views.leave_club, name='leave_club'),
    path('create_club/', views.CreateClubView.as_view(), name='create_club'),
    path('transfer_ownership/<int:user_id>/<int:club_id>', views.TransferClubLeadership.as_view(), name='transfer_ownership'),
    path('forum/<int:club_id>', views.ClubForumView.as_view(), name='club_forum'),
    path('new_post/<int:club_id>', views.NewPostView.as_view(), name='new_post'),
    path('accept_request/<int:user_id>', views.accept_request, name='accept_request'),
    path('reject_request/<int:user_id>', views.reject_request, name='reject_request'),
]
