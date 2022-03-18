from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth import get_user_model
from utilties.token_generator import generate_token
from .forms import UserRegistrationForm, ResendActivationForm, LoginForm, PWResetForm, PWResetConfirmForm, \
    ProfileEditForm, PWChangeForm, AddBalanceForm
from utilties.email_utils import send_activation_email
from django.views import View
from utilties.messaging import get_message
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AssertNotLoggedInMixin
from utilties.payment import start_payment
_User = get_user_model()


class UserCreationView(AssertNotLoggedInMixin, FormView):
    template_name = 'registration_page.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    redirect_url = 'login'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activation_email(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, get_message('authentication/account_created'))
        messages.add_message(self.request, messages.INFO, get_message('authentication/activate_your_account'))
        return super().form_valid(form)


class AccountActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = _User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, _User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, get_message('authentication/activation_success'))
        else:
            messages.add_message(request, messages.ERROR, get_message('authentication/activation_failed'))
        return redirect('login')


class ReSendActivationLinkView(AssertNotLoggedInMixin, FormView):
    template_name = 'resend_activation.html'
    form_class = ResendActivationForm
    redirect_url = 'home'

    def form_valid(self, form):
        got_email = form.cleaned_data['email']
        send_activation_email(self.request, _User.objects.get(email=got_email))
        messages.add_message(self.request, messages.INFO, get_message('authentication/resend_activation'))
        return redirect('home')


class RequestResetPasswordView(auth_views.PasswordResetView):
    email_template_name = 'email/password_reset_email.html'
    template_name = 'password_reset.html'
    success_url = reverse_lazy('home')
    form_class = PWResetForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, get_message('authentication/password_reset_sent'))
        return super().form_valid(form)


class PasswordResetView(auth_views.PasswordResetConfirmView):
    template_name = 'set_new_password.html'
    success_url = reverse_lazy('login')
    form_class = PWResetConfirmForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, get_message('authentication/password_changed'))
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = 'login_page.html'
    form_class = LoginForm

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        return next_page if next_page else reverse_lazy('home')


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


class UserDashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_view.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile')
    template_name = 'edit_profile.html'

    def form_valid(self, form):
        if form.changed_data:
            messages.add_message(self.request, messages.SUCCESS, get_message('authentication/profile_edited'))
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    form_class = PWChangeForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, get_message('authentication/password_changed'))
        return super().form_valid(form)


class AddBalance(LoginRequiredMixin, FormView):
    template_name = 'add_balance.html'
    form_class = AddBalanceForm

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        return start_payment(self.request, amount, 'credit')


