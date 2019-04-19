from urllib.parse import urlparse, ParseResult, urlunparse

from django.template import Context, Library
from django.urls import resolve, reverse, NoReverseMatch

register = Library()


@register.simple_tag(takes_context=True)
def url_extend(context: Context, *args, **kwargs):
    current_url = context["request"].get_full_path()
    resolved = resolve(current_url)

    url = resolved.url_name
    app_name = resolved.app_name

    try:
        _args = resolved.args
        _kwargs = resolved.kwargs.copy()

        _args += args
        _kwargs.update(kwargs)

        if app_name:
            pattern = f"{app_name}:{url}"
        else:
            pattern = url

        return reverse(pattern, args=_args, kwargs=_kwargs)
    except NoReverseMatch:
        _args = resolved.args
        _kwargs = resolved.kwargs.copy()

        if app_name:
            pattern = f"{app_name}:{url}"
        else:
            pattern = url

        reversed_url = reverse(pattern, args=_args, kwargs=_kwargs)
        parsed: ParseResult = urlparse(reversed_url)

        params = parsed.params

        if params:
            params += f"&"
        else:
            params = "?"

        params += "&".join(args)
        kwarg_list = []

        for key, value in kwargs.items():
            kwarg_list.append(f"{key}={value}")

        params += "&".join(kwarg_list)

        parsed = ParseResult(
            parsed.scheme, parsed.netloc, parsed.path,
            "", parsed.query, parsed.fragment
        )

        unparsed = urlunparse(parsed) + params
        print(parsed)
        print(unparsed)
        return unparsed
