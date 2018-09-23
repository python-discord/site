from django.core.exceptions import ValidationError
from django.test import TestCase

from ..validators import validate_tag_embed


REQUIRED_KEYS = (
    'content', 'fields', 'image', 'title', 'video'
)


class TagEmbedValidatorTests(TestCase):
    def test_rejects_non_mapping(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed('non-empty non-mapping')

    def test_rejects_missing_required_keys(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'unknown': "key"
            })

    def test_rejects_one_correct_one_incorrect(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'provider': "??",
                'title': ""
            })

    def test_rejects_empty_required_key(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': ''
            })

    def test_rejects_list_as_embed(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed([])

    def test_rejects_required_keys_and_unknown_keys(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "the duck walked up to the lemonade stand",
                'and': "he said to the man running the stand"
            })

    def test_rejects_too_long_title(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': 'a' * 257
            })

    def test_rejects_too_many_fields(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'fields': [{} for _ in range(26)]
            })

    def test_rejects_too_long_description(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'description': 'd' * 2049
            })

    def test_allows_valid_embed(self):
        validate_tag_embed({
            'title': "My embed",
            'description': "look at my embed, my embed is amazing"
        })

    def test_allows_unvalidated_fields(self):
        validate_tag_embed({
            'title': "My embed",
            'provider': "what am I??"
        })

    def test_rejects_fields_as_list_of_non_mappings(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'fields': ['abc']
            })

    def test_rejects_fields_with_unknown_fields(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'fields': [
                    {
                        'what': "is this field"
                    }
                ]
            })

    def test_rejects_fields_with_too_long_name(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'fields': [
                    {
                        'name': "a" * 257
                    }
                ]
            })

    def test_rejects_one_correct_one_incorrect_field(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'fields': [
                    {
                        'name': "Totally valid",
                        'value': "LOOK AT ME"
                    },
                    {
                        'oh': "what is this key?"
                    }
                ]
            })

    def test_allows_valid_fields(self):
        validate_tag_embed({
            'fields': [
                {
                    'name': "valid",
                    'value': "field"
                }
            ]
        })

    def test_rejects_footer_as_non_mapping(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'footer': []
            })

    def test_rejects_footer_with_unknown_fields(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'footer': {
                    'duck': "quack"
                }
            })

    def test_rejects_footer_with_empty_text(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'footer': {
                    'text': ""
                }
            })

    def test_allows_footer_with_proper_values(self):
        validate_tag_embed({
            'title': "whatever",
            'footer': {
                'text': "django good"
            }
        })

    def test_rejects_author_as_non_mapping(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'author': []
            })

    def test_rejects_author_with_unknown_field(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'author': {
                    'field': "that is unknown"
                }
            })

    def test_rejects_author_with_empty_name(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'author': {
                    'name': ""
                }
            })

    def test_rejects_author_with_one_correct_one_incorrect(self):
        with self.assertRaises(ValidationError):
            validate_tag_embed({
                'title': "whatever",
                'author': {
                    # Relies on "dictionary insertion order remembering" (D.I.O.R.) behaviour
                    'url': "bobswebsite.com",
                    'name': ""
                }
            })

    def test_allows_author_with_proper_values(self):
        validate_tag_embed({
            'title': "whatever",
            'author': {
                'name': "Bob"
            }
        })
