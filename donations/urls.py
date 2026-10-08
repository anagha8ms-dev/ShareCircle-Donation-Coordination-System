from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('add/',views.add_donation,name='add_donation'),
    path('login/',views.user_login,name='login'),
    path('list/',views.donation_list,name='donation_list'),
    path('edit/<int:id>/',views.edit_donation,name='edit_donation'),
    path('delete/<int:pk>/',views.delete_donation,name='delete_donation'),
    path('register/',views.register,name='register'),
    path('donor_dashboard/',views.donor_dashboard,name='donor_dashboard'),
    path('recipient_dashboard/',views.recipient_dashboard,name='recipient_dashboard'),
    path('logout/',views.user_logout,name='logout'),
    path('request-donation/<int:donation_id>/',views.request_donation,name='request_donation'),
    path('donation-request/',views.donation_requests,name='donation_requests'),
    path('accept-request/<int:request_id>/',views.accept_request,name='accept_request'),
    path('request/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('request/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('my-requests/',views.my_requests,name='my_requests'),
    path('forgot-password/',auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_confirm.html'),name='password_reset_confirm'),
    path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_cmplt.html'),name='password_reset_complete'),
    path('index', views.index, name='index'),

    
]