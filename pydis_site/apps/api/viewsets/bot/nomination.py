from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot import Nomination
from pydis_site.apps.api.serializers import NominationSerializer


class NominationViewSet(ModelViewSet):
    # TODO: doc me
    serializer_class = NominationSerializer
    queryset = Nomination.objects.prefetch_related('author', 'user')
    frozen_fields = ('author', 'inserted_at', 'user')

    def update(self, request, *args, **kwargs):
        """
        DRF method for updating a Nomination.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """

        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
