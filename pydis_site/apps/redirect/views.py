import typing as t

from django.views.generic import RedirectView


class CustomRedirectView(RedirectView):
    """Extended RedirectView for manual route args."""

    # We want temporary redirects for the time being, after this is running on prod and
    # stable we can enable permanent redirects.
    permanent = False
    static_args = ()
    prefix_redirect = False

    @classmethod
    def as_view(cls, **initkwargs):
        """Overwrites original as_view to add static args."""
        return super().as_view(**initkwargs)

    def get_redirect_url(self, *args, **kwargs) -> t.Optional[str]:
        """Extends default behaviour to use static args."""
        args = self.static_args + args + tuple(kwargs.values())
        if self.prefix_redirect:
            args = ("".join(args),)

        return super().get_redirect_url(*args)
