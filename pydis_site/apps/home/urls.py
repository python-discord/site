from allauth.account.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.messages import ERROR
from django.urls import include, path

from pydis_site.utils.views import MessageRedirectView
from .views import AccountDeleteView, AccountSettingsView, HomeView, timeline

app_name = 'home'
urlpatterns = [
    # We do this twice because Allauth expects specific view names to exist
    path('', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='socialaccount_connections'),

    path('pages/', include('wiki.urls')),

    path('accounts/', include('allauth.socialaccount.providers.discord.urls')),
    path('accounts/', include('allauth.socialaccount.providers.github.urls')),

    path(
        'accounts/login/cancelled', MessageRedirectView.as_view(
            pattern_name="home", message="Login cancelled."
        ), name='socialaccount_login_cancelled'
    ),
    path(
        'accounts/login/error', MessageRedirectView.as_view(
            pattern_name="home", message="Login encountered an unknown error, please try again.",
            message_level=ERROR
        ), name='socialaccount_login_error'
    ),

    path('accounts/settings', AccountSettingsView.as_view(), name="account_settings"),
    path('accounts/delete', AccountDeleteView.as_view(), name="account_delete"),

    path('logout', LogoutView.as_view(), name="logout"),

    path('admin/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
    path('timeline/', timeline, name="timeline"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
