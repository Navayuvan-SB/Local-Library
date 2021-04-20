from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CustomSignupForm


def sign_up_user(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('events'))

    if request.method == 'POST':

        form = CustomSignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            new_user = User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name)

            return HttpResponseRedirect(reverse('login'))

    else:
        form = CustomSignupForm()

    context = {
        'form': form
    }

    return render(request, 'registration/sign_up_user.html', context)
