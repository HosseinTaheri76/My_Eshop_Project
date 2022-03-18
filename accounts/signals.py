from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from utilties.messaging import get_message


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, get_message('authentication/logged_out'))


@receiver(user_logged_in)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.SUCCESS, get_message('authentication/logged_in'))
