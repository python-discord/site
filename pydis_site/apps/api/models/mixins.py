from operator import itemgetter

from django.db import models


class ModelReprMixin:
    """Mixin providing a `__repr__()` to display model class name and initialisation parameters."""

    def __repr__(self):
        """Returns the current model class name and initialisation parameters."""
        attributes = ' '.join(
            f'{attribute}={value!r}'
            for attribute, value in sorted(
                self.__dict__.items(),
                key=itemgetter(0)
            )
            if not attribute.startswith('_')
        )
        return f'<{self.__class__.__name__}({attributes})>'


class ModelTimestampMixin(models.Model):
    """Mixin providing created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Metaconfig for the mixin."""

        abstract = True
