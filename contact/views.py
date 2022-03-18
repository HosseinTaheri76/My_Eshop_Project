from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactUsForm
from utilties.messaging import get_message
from django.contrib import messages


class ContactUsView(View):
    def get(self, request):
        initial_data = {}
        if request.user.is_authenticated:
            user = request.user
            form_initial = {
                'email': user.email,
                'full_name': user.full_name,
            }
            if user.phone:
                form_initial.update({'phone': user.phone})
            initial_data = form_initial
        form = ContactUsForm(initial=initial_data, request=request)
        return render(request, 'contact_us.html', {'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, get_message('contact_us/message_sent'))
            return redirect('home')
        return render(request, 'contact_us.html', {'form': form})
