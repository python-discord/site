from allauth.account.views import LogoutView
from allauth.socialaccount.views import ConnectionsView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.messages import ERROR
from django.urls import include, path

from pydis_site.apps.home.views.login import LoginView
from pydis_site.utils.views import MessageRedirectView
from .views import HomeView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
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
            pattern_name="home", message="Login failed due to an error, please try again.",
            message_level=ERROR
        ), name='socialaccount_login_error'
    ),

    path('connections', ConnectionsView.as_view()),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

    path('admin/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
