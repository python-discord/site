from django.views.generic import RedirectView


class CustomRedirectView(RedirectView):
    """Extended RedirectView for manual route args."""

    permanent = True
    static_args = ()

    @classmethod
    def as_view(cls, **initkwargs):
        """Overwrites original as_view to add static args."""
        return super().as_view(**initkwargs)

    def get_redirect_url(self, *args, **kwargs):
        """Extends default behaviour to use static args."""
        args = args + self.static_args
        return super().get_redirect_url(*args, **kwargs)
