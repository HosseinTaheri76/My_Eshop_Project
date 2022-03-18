from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from threading import Thread
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .token_generator import generate_token


class MailSender:

    def __init__(self, subject, to, template_name, context):
        self.subject = subject
        self.to = to
        self.template_name = template_name
        self.context = context

    def send(self):
        html_message = render_to_string(self.template_name, self.context)
        plain_text = strip_tags(html_message)
        send_mail(
            subject=self.subject,
            message=plain_text,
            from_email='djangotest.maham@gmail.com',
            recipient_list=self.to,
            html_message=html_message
        )


class EmailThread(Thread):

    def __init__(self, mail):
        super().__init__()
        self.mail = mail

    def run(self):
        self.mail.send()


def send_activation_email(request, user):
    email_context = {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    subject = 'لطفا حساب کاربری خود را فعال کنید.'
    mail = MailSender(subject, [user.email], 'email/activation_email.html', email_context)
    EmailThread(mail).start()


def send_reply_email(user_fullname, user_email, user_msg_title, admin_answer):
    subject = 'پاسخ پیام شما'
    template_name = 'email/message_reply.html'
    email_context = {
        'full_name': user_fullname,
        'title': user_msg_title,
        'answer': admin_answer
    }
    mail = MailSender(subject, [user_email], template_name, email_context)
    EmailThread(mail).start()


def send_fav_product_state_change(product, state, recipient_list):
    subject = 'تغییر در وضعیت محصول مورد علاقه شما'
    msg = {
        'discounted': f' تخفیف خورد.{product}',
        'available': f' مجددا موجود شد.{product}'
    }
    template_name = 'email/fav_prod_state_change.html'
    email_context = {
        'msg': msg[state]
    }
    mail = MailSender(subject, recipient_list, template_name, email_context)
    EmailThread(mail).start()
