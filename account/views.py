from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.translation import templatize
from django.views.generic import CreateView

from .forms import RegistrationForm
from django.urls import reverse_lazy


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')


