from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from common.settings import NETWORK_USER_CUSTOM_FIELDS
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class SignInForm(ModelForm):
    username = forms.CharField(label='Pseudo',
                               widget=forms.TextInput(attrs={
                                   'class': "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
                                   'placeholder': 'Pseudo'
                               })
                               )
    password = forms.CharField(label='Mot de passe',
                               widget=forms.PasswordInput(attrs={
                                   'class': "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
                                   'placeholder': 'Mot de passe'
                               })
                               )
    class Meta:
        model = Profile
        fields = ('username', 'password')


class SignUpForm(ModelForm):
    """
    A form for user that allow them to sign up
    """
    first_name = forms.CharField(label='Prénom',
                                 widget=forms.TextInput(attrs={
                                     'class': "appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
                                                        )
                                 )
    last_name = forms.CharField(label='Nom',
                                 widget=forms.TextInput(attrs={
                                     'class': "appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
                                                        )
                                 )
    username = forms.CharField(label='Pseudo',
                                 widget=forms.TextInput(attrs={
                                     'class': "appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
                                                        )
                                 )
    email = forms.CharField(label='Email',
                                 widget=forms.EmailInput(attrs={
                                     'class': "appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
                                                        )
                                 )
    password = forms.CharField(label='Mot de passe',
                                 widget=forms.PasswordInput(attrs={
                                     'class': "appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
                                                        )
                                 )
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user = super().save(commit=True)
        return user


class UserAdminCreationForm(ModelForm):
    """
    A form for creating new users. Includes all the required
    fields
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'first_name', 'last_name',
                  'password', 'is_superuser', 'is_staff', 'accepted']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user = super().save(commit=True)
        return user


class UserAdminChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    widgets = {'birth_date': forms.DateInput(attrs={'type':'date'})}
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'password', 'accepted',
                  'is_superuser', 'is_staff', 'birth_date', 'location']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
