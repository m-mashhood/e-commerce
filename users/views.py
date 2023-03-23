from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, View

from users.forms import LoginForm, SignUpForm

from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class LoginPageView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.category == User.BUYER[0]:
                return redirect('all_list_products')
            else:
                return redirect('list_products')
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                if user.category == User.BUYER[0]:
                    return redirect('all_list_products')
                else:
                    return redirect('list_products')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class LogoutView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = 'Logged out successfully!'
        if self.request.user.is_authenticated:
            logout(self.request)
        return render(request, self.template_name, context={'form': form, 'message': message})

