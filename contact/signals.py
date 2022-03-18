from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserMessage
from utilties.email_utils import send_reply_email as _send_email


@receiver(post_save, sender=UserMessage)
def send_replay_mail(sender, instance, created, **kwargs):
    if not created:
        if instance.tracker.has_changed('is_answered') and instance.is_answered:
            if instance.answer_text:
                _send_email(
                    instance.full_name,
                    instance.email,
                    instance.title,
                    instance.answer_text
                )
