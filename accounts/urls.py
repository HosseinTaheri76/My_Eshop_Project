from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.AccountActivationView.as_view(), name='activate'),
    path('resend_activation/', views.ReSendActivationLinkView.as_view(), name='resend_activation'),
    path('password_reset/', views.RequestResetPasswordView.as_view(), name='password_reset'),
    path('set_new_password/<uidb64>/<token>/', views.PasswordResetView.as_view(), name='password_reset_confirm'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserDashBoardView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit-profile'),
    path('profile/change_password/', views.PasswordChangeView.as_view(), name='change_password'),
    path('add_balance', views.AddBalance.as_view(), name='add_balance'),
]
