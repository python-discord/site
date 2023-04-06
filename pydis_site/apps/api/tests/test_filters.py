import contextlib
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, Tuple, Type

from django.db.models import Model
from django.urls import reverse

from pydis_site.apps.api.models.bot.filters import Filter, FilterList
from pydis_site.apps.api.tests.base import AuthenticatedAPITestCase


@dataclass()
class TestSequence:
    model: Type[Model]
    route: str
    object: Dict[str, Any]
    ignored_fields: Tuple[str, ...] = ()

    def url(self, detail: bool = False) -> str:
        return reverse(f'api:bot:{self.route}-{"detail" if detail else "list"}')


FK_FIELDS: Dict[Type[Model], Tuple[str, ...]] = {
    FilterList: (),
    Filter: ("filter_list",),
}


def get_test_sequences() -> Dict[str, TestSequence]:
    filter_list1_deny_dict = {
        "name": "testname",
        "list_type": 0,
        "guild_pings": [],
        "filter_dm": True,
        "dm_pings": [],
        "remove_context": False,
        "bypass_roles": [],
        "enabled": True,
        "dm_content": "",
        "dm_embed": "",
        "infraction_type": "NONE",
        "infraction_reason": "",
        "infraction_duration": timedelta(seconds=0),
        "infraction_channel": 0,
        "disabled_channels": [],
        "disabled_categories": [],
        "enabled_channels": [],
        "enabled_categories": [],
        "send_alert": True
    }
    filter_list1_allow_dict = filter_list1_deny_dict.copy()
    filter_list1_allow_dict["list_type"] = 1
    filter_list1_allow = FilterList(**filter_list1_allow_dict)

    return {
        "filter_list1": TestSequence(
            FilterList,
            "filterlist",
            filter_list1_deny_dict,
            ignored_fields=("filters", "created_at", "updated_at")
        ),
        "filter_list2": TestSequence(
            FilterList,
            "filterlist",
            {
                "name": "testname2",
                "list_type": 1,
                "guild_pings": ["Moderators"],
                "filter_dm": False,
                "dm_pings": ["here"],
                "remove_context": True,
                "bypass_roles": ["123456"],
                "enabled": False,
                "dm_content": "testing testing",
                "dm_embed": "one two three",
                "infraction_type": "TIMEOUT",
                "infraction_reason": "stop testing",
                "infraction_duration": timedelta(seconds=10.5),
                "infraction_channel": 123,
                "disabled_channels": ["python-general"],
                "disabled_categories": ["CODE JAM"],
                "enabled_channels": ["mighty-mice"],
                "enabled_categories": ["Lobby"],
                "send_alert": False
            },
            ignored_fields=("filters", "created_at", "updated_at")
        ),
        "filter": TestSequence(
            Filter,
            "filter",
            {
                "content": "bad word",
                "description": "This is a really bad word.",
                "additional_settings": "{'hi': 'there'}",
                "guild_pings": None,
                "filter_dm": None,
                "dm_pings": None,
                "remove_context": None,
                "bypass_roles": None,
                "enabled": None,
                "dm_content": None,
                "dm_embed": None,
                "infraction_type": None,
                "infraction_reason": None,
                "infraction_duration": None,
                "infraction_channel": None,
                "disabled_channels": None,
                "disabled_categories": None,
                "enabled_channels": None,
                "enabled_categories": None,
                "send_alert": None,
                "filter_list": filter_list1_allow
            },
            ignored_fields=("created_at", "updated_at")
        ),
    }


def save_nested_objects(object_: Model, save_root: bool = True) -> None:
    for field in FK_FIELDS.get(object_.__class__, ()):
        value = getattr(object_, field)
        save_nested_objects(value)

    if save_root:
        object_.save()


def clean_test_json(json: dict) -> dict:
    for key, value in json.items():
        if isinstance(value, Model):
            json[key] = value.id
        elif isinstance(value, timedelta):
            json[key] = str(value.total_seconds())

    return json


def clean_api_json(json: dict, sequence: TestSequence) -> dict:
    for field in sequence.ignored_fields + ("id",):
        with contextlib.suppress(KeyError):
            del json[field]

    return json


def flatten_settings(json: dict) -> dict:
    settings = json.pop("settings", {})
    flattened_settings = {}
    for entry, value in settings.items():
        if isinstance(value, dict):
            flattened_settings.update(value)
        else:
            flattened_settings[entry] = value

    json.update(flattened_settings)

    return json


class GenericFilterTests(AuthenticatedAPITestCase):

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
                    clean_api_json(flatten_settings(response.json()[0]), sequence)
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
                    clean_api_json(flatten_settings(response.json()), sequence)
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
                    clean_api_json(flatten_settings(response.json()), sequence),
                    clean_test_json(sequence.object)
                )

    def test_creation_missing_field(self) -> None:
        for name, sequence in get_test_sequences().items():
            ignored_fields = sequence.ignored_fields + ("id", "additional_settings")
            with self.subTest(name=name):
                saved = sequence.model(**sequence.object)
                save_nested_objects(saved)
                data = clean_test_json(sequence.object.copy())

                for field in sequence.model._meta.get_fields():
                    with self.subTest(field=field):
                        if field.null or field.name in ignored_fields:
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


class FilterValidationTests(AuthenticatedAPITestCase):

    def test_filter_validation(self) -> None:
        test_sequences = get_test_sequences()
        base_filter = test_sequences["filter"]
        base_filter_list = test_sequences["filter_list1"]
        cases = (
            ({"infraction_reason": "hi"}, {}, 400),
            ({"infraction_duration": timedelta(seconds=10)}, {}, 400),
            ({"infraction_reason": "hi"}, {"infraction_type": "NOTE"}, 200),
            ({"infraction_type": "TIMEOUT", "infraction_duration": timedelta(days=30)}, {}, 400),
            ({"infraction_duration": timedelta(seconds=10)}, {"infraction_type": "TIMEOUT"}, 200),
            ({"enabled_channels": ["admins"]}, {}, 200),
            ({"disabled_channels": ["123"]}, {}, 200),
            ({"enabled_categories": ["CODE JAM"]}, {}, 200),
            ({"disabled_categories": ["CODE JAM"]}, {}, 200),
            ({"enabled_channels": ["admins"], "disabled_channels": ["123", "admins"]}, {}, 400),
            ({"enabled_categories": ["admins"], "disabled_categories": ["123", "admins"]}, {}, 400),
            ({"enabled_channels": ["admins"]}, {"disabled_channels": ["123", "admins"]}, 400),
            ({"enabled_categories": ["admins"]}, {"disabled_categories": ["123", "admins"]}, 400),
        )

        for filter_settings, filter_list_settings, response_code in cases:
            with self.subTest(
                f_settings=filter_settings, fl_settings=filter_list_settings, response=response_code
            ):
                base_filter.model.objects.all().delete()
                base_filter_list.model.objects.all().delete()

                case_filter_dict = base_filter.object.copy()
                case_fl_dict = base_filter_list.object.copy()
                case_fl_dict.update(filter_list_settings)

                case_fl = base_filter_list.model(**case_fl_dict)
                case_filter_dict["filter_list"] = case_fl
                case_filter = base_filter.model(**case_filter_dict)
                save_nested_objects(case_filter)

                filter_settings["filter_list"] = case_fl
                response = self.client.patch(
                    f"{base_filter.url()}/{case_filter.id}", data=clean_test_json(filter_settings)
                )
                self.assertEqual(response.status_code, response_code)

    def test_filter_list_validation(self) -> None:
        test_sequences = get_test_sequences()
        base_filter_list = test_sequences["filter_list1"]
        cases = (
            ({"infraction_reason": "hi"}, 400),
            ({"infraction_duration": timedelta(seconds=10)}, 400),
            ({"infraction_type": "TIMEOUT", "infraction_duration": timedelta(days=30)}, 400),
            ({"infraction_reason": "hi", "infraction_type": "NOTE"}, 200),
            ({"infraction_duration": timedelta(seconds=10), "infraction_type": "TIMEOUT"}, 200),
            ({"enabled_channels": ["admins"]}, 200), ({"disabled_channels": ["123"]}, 200),
            ({"enabled_categories": ["CODE JAM"]}, 200),
            ({"disabled_categories": ["CODE JAM"]}, 200),
            ({"enabled_channels": ["admins"], "disabled_channels": ["123", "admins"]}, 400),
            ({"enabled_categories": ["admins"], "disabled_categories": ["123", "admins"]}, 400),
        )

        for filter_list_settings, response_code in cases:
            with self.subTest(fl_settings=filter_list_settings, response=response_code):
                base_filter_list.model.objects.all().delete()

                case_fl_dict = base_filter_list.object.copy()
                case_fl = base_filter_list.model(**case_fl_dict)
                save_nested_objects(case_fl)

                response = self.client.patch(
                    f"{base_filter_list.url()}/{case_fl.id}",
                    data=clean_test_json(filter_list_settings)
                )
                self.assertEqual(response.status_code, response_code)

    def test_filter_unique_constraint(self) -> None:
        test_filter = get_test_sequences()["filter"]
        test_filter.model.objects.all().delete()
        test_filter_object = test_filter.model(**test_filter.object)
        save_nested_objects(test_filter_object, False)

        response = self.client.post(test_filter.url(), data=clean_test_json(test_filter.object))
        self.assertEqual(response.status_code, 201)

        response = self.client.post(test_filter.url(), data=clean_test_json(test_filter.object))
        self.assertEqual(response.status_code, 400)
