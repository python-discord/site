from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot import Nomination
from pydis_site.apps.api.serializers import NominationSerializer


class NominationViewSet(ModelViewSet):
    # TODO: doc me
    serializer_class = NominationSerializer
    queryset = Nomination.objects.prefetch_related('actor', 'user')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('user__id', 'actor__id', 'active')
    frozen_fields = ('id', 'actor', 'inserted_at', 'user', 'unwatched_at', 'active')
    frozen_on_create = ('unwatched_at', 'unnominate_reason')

    def create(self, request, *args, **kwargs):
        for field in request.data:
            if field in self.frozen_on_create:
                raise ValidationError({field: ['This field cannot be updated.']})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def end_nomination(self, request, pk=None):
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        if "unnominate_reason" not in request.data:
            raise ValidationError(
                {'unnominate_reason': ['This field is required when ending a nomination']}
            )

        instance = self.get_object()
        if not instance.active:
            raise ValidationError({'active': ['A nomination must be active to be ended.']})

        instance.active = False
        instance.unwatched_at = timezone.now()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.save()

        return Response(serializer.data)
