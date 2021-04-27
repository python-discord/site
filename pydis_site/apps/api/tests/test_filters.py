import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Type

from django.db.models import Model
from django_hosts import reverse

from pydis_site.apps.api.models.bot.filters import (  # noqa: I101 - Preserving the filter order
    FilterList,
    FilterSettings,
    FilterAction,
    ChannelRange,
    Filter,
    FilterOverride
)
from pydis_site.apps.api.tests.base import APISubdomainTestCase


@dataclass()
class TestSequence:
    model: Type[Model]
    route: str
    object: Dict[str, Any]
    ignored_fields: Tuple[str] = ()

    def url(self, detail: bool = False) -> str:
        return reverse(f'bot:{self.route}-{"detail" if detail else "list"}', host='api')


FK_FIELDS: Dict[Type[Model], Tuple[str]] = {
    FilterList: ("default_settings",),
    FilterSettings: ("default_action", "default_range"),
    FilterAction: (),
    ChannelRange: (),
    Filter: (),
    FilterOverride: ("filter_action", "filter_range")
}


def get_test_sequences() -> Dict[str, TestSequence]:
    return {
        "filter_list": TestSequence(
            FilterList,
            "filterlist",
            {
                "name": "testname",
                "list_type": 0,
                "default_settings": FilterSettings(
                    ping_type=[],
                    filter_dm=False,
                    dm_ping_type=[],
                    delete_messages=False,
                    bypass_roles=[],
                    enabled=False,
                    default_action=FilterAction(
                        user_dm=None,
                        infraction_type=None,
                        infraction_reason="",
                        infraction_duration=None
                    ),
                    default_range=ChannelRange(
                        disallowed_channels=[],
                        disallowed_categories=[],
                        allowed_channels=[],
                        allowed_category=[],
                        default=False
                    )
                )
            },
            ignored_fields=("filters",)
        ),
        "filter_settings": TestSequence(
            FilterSettings,
            "filtersettings",
            {
                "ping_type": ["onduty"],
                "filter_dm": True,
                "dm_ping_type": ["123456"],
                "delete_messages": True,
                "bypass_roles": [123456],
                "enabled": True,
                "default_action": FilterAction(
                    user_dm=None,
                    infraction_type=None,
                    infraction_reason="",
                    infraction_duration=None
                ),
                "default_range": ChannelRange(
                    disallowed_channels=[],
                    disallowed_categories=[],
                    allowed_channels=[],
                    allowed_category=[],
                    default=False
                )
            }
        ),
        "filter_action": TestSequence(
            FilterAction,
            "filteraction",
            {
                "user_dm": "This is a DM message.",
                "infraction_type": "Mute",
                "infraction_reason": "Too long beard",
                "infraction_duration": "1 02:03:00"
            }
        ),
        "channel_range": TestSequence(
            ChannelRange,
            "channelrange",
            {
                "disallowed_channels": [1234],
                "disallowed_categories": [5678],
                "allowed_channels": [9101],
                "allowed_category": [1121],
                "default": True
            }
        ),
        "filter": TestSequence(
            Filter,
            "filter",
            {
                "content": "bad word",
                "description": "This is a really bad word.",
                "additional_field": None,
                "override": None
            }
        ),
        "filter_override": TestSequence(
            FilterOverride,
            "filteroverride",
            {
                "ping_type": ["everyone"],
                "filter_dm": False,
                "dm_ping_type": ["here"],
                "delete_messages": False,
                "bypass_roles": [9876],
                "enabled": True,
                "filter_action": None,
                "filter_range": None
            }
        )
    }


def save_nested_objects(object_: Model, save_root: bool = True) -> None:
    for field in FK_FIELDS[object_.__class__]:
        value = getattr(object_, field)

        if value is not None:
            save_nested_objects(value)

    if save_root:
        object_.save()


def clean_test_json(json: dict) -> dict:
    for key, value in json.items():
        if isinstance(value, Model):
            json[key] = value.id

    return json


def clean_api_json(json: dict, sequence: TestSequence) -> dict:
    for field in sequence.ignored_fields + ("id",):
        with contextlib.suppress(KeyError):
            del json[field]

    return json


class GenericFilterTest(APISubdomainTestCase):
    def test_cannot_read_unauthenticated(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                self.client.force_authenticate(user=None)

                response = self.client.get(sequence.url())
                self.assertEqual(response.status_code, 401)

    def test_empty_database(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                response = self.client.get(sequence.url())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), [])

    def test_fetch(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                save_nested_objects(sequence.model(**sequence.object))

                response = self.client.get(sequence.url())
                self.assertDictEqual(
                    clean_test_json(sequence.object),
                    clean_api_json(response.json()[0], sequence)
                )

    def test_fetch_by_id(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                saved = sequence.model(**sequence.object)
                save_nested_objects(saved)

                response = self.client.get(f"{sequence.url()}/{saved.id}")
                self.assertDictEqual(
                    clean_test_json(sequence.object),
                    clean_api_json(response.json(), sequence)
                )

    def test_fetch_non_existing(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                response = self.client.get(f"{sequence.url()}/42")
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(response.json(), {'detail': 'Not found.'})

    def test_creation(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                save_nested_objects(sequence.model(**sequence.object), False)
                data = clean_test_json(sequence.object.copy())
                response = self.client.post(sequence.url(), data=data)

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(
                    clean_api_json(response.json(), sequence),
                    clean_test_json(sequence.object)
                )

    def test_creation_missing_field(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                save_nested_objects(sequence.model(**sequence.object), False)
                data = clean_test_json(sequence.object.copy())

                for field in sequence.model._meta.get_fields():
                    with self.subTest(field=field):
                        if field.null or field.name in sequence.ignored_fields + ("id",):
                            continue

                        test_data = data.copy()
                        del test_data[field.name]

                        response = self.client.post(sequence.url(), data=test_data)
                        self.assertEqual(response.status_code, 400)

    def test_deletion(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                saved = sequence.model(**sequence.object)
                save_nested_objects(saved)

                response = self.client.delete(f"{sequence.url()}/{saved.id}")
                self.assertEqual(response.status_code, 204)

    def test_deletion_non_existing(self) -> None:
        for name, sequence in get_test_sequences().items():
            with self.subTest(name=name):
                sequence.model.objects.all().delete()

                response = self.client.delete(f"{sequence.url()}/42")
                self.assertEqual(response.status_code, 404)

    def test_reject_invalid_ping(self) -> None:
        url = reverse('bot:filteroverride-list', host='api')
        data = {
            "ping_type": ["invalid"]
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'ping_type': ["'invalid' isn't a valid ping type."]})
