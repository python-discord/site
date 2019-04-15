from operator import itemgetter


class ModelReprMixin:
    """
    Adds a `__repr__` method to the model subclassing this
    mixin which will display the model's class name along
    with all parameters used to construct the object.
    """

    def __repr__(self):
        attributes = ' '.join(
            f'{attribute}={value!r}'
            for attribute, value in sorted(
                self.__dict__.items(),
                key=itemgetter(0)
            )
            if not attribute.startswith('_')
        )
        return f'<{self.__class__.__name__}({attributes})>'
