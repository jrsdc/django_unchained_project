from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Inbox
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:msg_id>/', views.inbox, name='inbox_detail'),  # Added for switching inbox msgs
    
    # Sent
    path('sent/', views.sent_messages, name='sent_messages'),
    path('sent/<int:msg_id>/', views.sent_messages, name='sent_detail'), # Added for switching sent msgs
    
    # Drafts
    path('drafts/', views.drafts, name='drafts'),
    path('drafts/<int:msg_id>/', views.drafts, name='draft_detail'),
    
    # Message Actions
    path('new/', views.new_message, name='new_message'),
    path('new/<int:draft_id>/', views.new_message, name='new_message_with_draft'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # Login / Logout / Register
    path('login/', auth_views.LoginView.as_view(template_name='user_messages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Password Reset Logic
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user_messages/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_messages/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_messages/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_messages/password_reset_complete.html'), name='password_reset_complete'),

    # Sidebar
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_page, name='settings'),
    path('teams/', views.teams_page, name='teams'),
]