from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy
from mysite import settings
from .forms import CustomPasswordResetForm
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home_view, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:university_id>/", views.user_profile_view, name="user_profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path("community/", views.community_view, name="community"),
    path("discussion/<int:discussion_id>/", views.discussion_detail, name="discussion_detail"),

    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/invite/', views.invite_member, name='invite_member'),
    path('groups/invitation/<int:invitation_id>/<str:action>/', views.respond_invitation, name='respond_invitation'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/<int:group_id>/remove_member/<int:user_id>/', views.remove_member, name='remove_member'),

    path('problems/', views.problems_view, name='problems'),  # problem list
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problems/crud/', views.problem_crud, name='problem_crud'),  # add new
    path('problems/crud/<int:pk>/', views.problem_crud, name='problem_crud'),  # edit existing
    path('problems/delete/<int:pk>/', views.problem_delete, name='problem_delete'),
    path('problems/<int:pk>/submit/', views.submit_solution, name='submit_solution'),

    path('submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),

    path('contests/', views.contest_list, name='contest_list'),
    path('create/', views.contest_create, name='contest_create'),
    path('contests/<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('contests/<int:contest_id>/register/', views.contest_register, name='contest_register'),

    path('contests/<int:contest_id>/problems/', views.contest_problems, name='contest_problems'),
    path('contests/<int:contest_id>/problems/<int:problem_id>/', views.contest_problem_detail, name='contest_problem_detail'),

    path('contests/<int:contest_id>/start/', views.start_contest, name='start_contest'),
    path('<int:contest_id>/update/', views.contest_update, name='contest_update'),
    path('<int:contest_id>/delete/', views.contest_delete, name='contest_delete'),
    path('contests/<int:contest_id>/submissions/', views.contest_submission_list, name='contest_submission_list'),
    path('contests/<int:contest_id>/submissions/<int:submission_id>/', views.contest_submission_detail, name='contest_submission_detail'),
    path('contests/<int:contest_id>/standings/', views.contest_standings, name='contest_standings'),

    path('about/', lambda request: render(request, 'about_developers.html'), name='about_developers'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='password_generic.html',
        extra_context={
            'title': 'Reset Password',
            'heading': 'Reset Your Password',
            'message': 'Enter your email to receive password reset instructions.',
            'button_text': 'Send Reset Email',
            'show_form': True,
            'extra_link_url': reverse_lazy('login'),  
            'extra_link_text': 'Return to Login',
        }
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_generic.html',
        extra_context={
            'title': 'Email Sent',
            'heading': 'Check Your Inbox',
            'message': 'We’ve emailed instructions to reset your password.',
            'show_form': False,
            'extra_link_url': reverse_lazy('login'),  
            'extra_link_text': 'Return to Login',
        }
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_generic.html',
        success_url=reverse_lazy('password_reset_complete'),
        extra_context={
            'title': 'Enter New Password',
            'heading': 'Set a New Password',
            'message': '',
            'button_text': 'Change Password',
            'show_form': True,
        }
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_generic.html',
        extra_context={
            'title': 'Password Reset Complete',
            'heading': 'Password Successfully Changed!',
            'message': 'You may now log in with your new password.',
            'show_form': False,
            'extra_link_url': reverse_lazy('login'),  
            'extra_link_text': 'Login Now',
        }
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)