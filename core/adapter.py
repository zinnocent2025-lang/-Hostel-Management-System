from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages


class MySocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        extra_data = sociallogin.account.extra_data

        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
        user.email = extra_data.get('email', '')

        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        picture = sociallogin.account.extra_data.get('picture', '')

        if picture:
            request.session['google_picture'] = picture

        return user