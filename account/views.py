from pprint import pprint

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Xin chào {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'login/register.html', {
        'form': form,
    })


class AccountDetailView(DetailView):
    model = User
    template_name = 'login/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)


class AccountUpdateView(UpdateView):
    model = User
    template_name = 'login/update.html'
    context_object_name = 'account'
    fields = ['first_name','last_name', 'email']
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)
