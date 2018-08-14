from django.conf import setting
from rest_framework import permissions


class HasValidAPIKey(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        return api_key == settings.BOT_API_KEY
