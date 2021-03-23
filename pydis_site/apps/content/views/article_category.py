import typing as t

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from pydis_site.apps.content import utils


class ArticleOrCategoryView(TemplateView):
    """Handles article and category pages."""

    def get_template_names(self) -> t.List[str]:
        """Checks does this use article template or listing template."""
        location = self.kwargs["location"].split("/")
        full_location = settings.ARTICLES_PATH.joinpath(*location)

        if full_location.is_dir():
            template_name = "content/listing.html"
        elif full_location.with_suffix(".md").is_file():
            template_name = "content/article.html"
        else:
            raise Http404

        return [template_name]

    def get_context_data(self, **kwargs) -> t.Dict[str, t.Any]:
        """Assign proper context variables based on what resource user requests."""
        context = super().get_context_data(**kwargs)

        location: list = self.kwargs["location"].split("/")
        full_location = settings.ARTICLES_PATH.joinpath(*location)

        if full_location.is_dir():
            context["category_info"] = utils.get_category(location)
            context["content"] = utils.get_articles(location)
            context["categories"] = utils.get_categories(location)
            # Add trailing slash here to simplify template
            context["path"] = "/".join(location) + "/"
            context["in_category"] = True
        elif full_location.with_suffix(".md").is_file():
            article_result = utils.get_article(location)

            if len(location) > 1:
                context["category_data"] = utils.get_category(location[:-1])
                context["category_data"]["raw_name"] = location[:-1][-1]
            else:
                context["category_data"] = {"name": None, "raw_name": None}

            context["article"] = article_result
            context["relevant_links"] = {
                link: value for link, value in zip(
                    article_result["metadata"].get("relevant_links", "").split(","),
                    article_result["metadata"].get("relevant_link_values", "").split(",")
                ) if link != "" and value != ""
            }
        else:
            raise Http404

        location.pop()
        breadcrumb_items = []
        while len(location):
            breadcrumb_items.insert(
                0,
                {
                    "name": utils.get_category(location)["name"],
                    "path": "/".join(location)
                }
            )
            location.pop()

        context["breadcrumb_items"] = breadcrumb_items

        return context
