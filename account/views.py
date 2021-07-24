from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from .forms import SignUpForm, SignInForm
from .decorator import login_excluded

class LoginView(TemplateView):
    """
    View of log in page
    """
    template_name = "account/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('profile')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        signin_form = SignInForm()
        signup_form = SignUpForm()
        return render(request, self.template_name,
                      {
                          'signin_form': signin_form,
                          'signup_form': signup_form,
                      })

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        signup_form = SignUpForm()
        signin_form = SignInForm(request.POST)
        if signin_form.is_valid():
            print('valid')
            user = signin_form.login(request)
            if user is not None:
                if user.accepted:
                    login(request, user)
                    return HttpResponseRedirect("profile")
                return HttpResponseRedirect("waiting")
        print('Not user')
        print(signin_form.errors)
        return render(request, self.template_name,
                      {
                          'signin_form': signin_form,
                          'signup_form': signup_form,
                      })

class SignUpView(TemplateView):
    """
    View of sign up page
    """
    template_name = "account/signup.html"
    login_template = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('profile')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    # def get(self, request, **kwargs):
    #     signup_form = SignUpForm()
    #     return render(request, self.template_name,
    #                   {
    #                       'signup_form': signup_form
    #                   })

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        signin_form = SignInForm()
        if signup_form.is_valid():
            signup_form.save()
            return HttpResponseRedirect("waiting")
        return render(request, self.login_template,
                      {
                          'signup_form': signup_form,
                          'signin_form': signin_form,
                          'modal': True
                      })


class WaitingView(TemplateView):
    """
    View of waiting page when user sign up
    """
    template_name = "account/waiting.html"
    def get(self, request, **kwargs):
        return render(request, self.template_name)

class ProfileView(TemplateView):
    """
    View of profile user
    """
    template_name = "account/profile.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name,
                      {
                          'user': request.user
                      })

class LogoutView(TemplateView):
    """
    View for logout user
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('login')