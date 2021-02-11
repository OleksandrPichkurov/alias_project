from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from datetime import timedelta
import datetime

from .models import Alias, alias_replace, get_aliases


# Create your tests here.


class AliasModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.alias = Alias.objects.create(
            alias='alias',
            target='sometarget',
            start=timezone.now()-timedelta(days=50),
            end=timezone.now()-timedelta(days=49)
        )
        cls.alias = Alias.objects.create(
            alias='new_alias',
            target='sometarget',
            start=timezone.now()-timedelta(days=48),
            end=timezone.now()-timedelta(days=47)
        )

    def test_save_alias_without_overlap(self):
        a = Alias.objects.create(
            alias='new_alias',
            target='sometarget',
            start=timezone.now()-timedelta(days=46)
        )
        self.assertEquals(str(self.alias), a.alias)

    def test_save_alias_with_overlap(self):
        with self.assertRaises(ValidationError):
            Alias.objects.create(
                alias='alias',
                target='sometarget',
                start=timezone.now()-timedelta(days=50)
            )

    def test_get_aliases(self):
        aliases = get_aliases(target='sometarget',
                              from_date=timezone.now()-timedelta(days=50),
                              to_date=datetime.datetime.max)
        self.assertEqual(len(aliases), 2)

    def test_alias_replace(self):
        alias = alias_replace(existing_alias='alias',
                              replace_at=datetime.datetime(2020, 5, 17),
                              new_alias_value='one_more_alias')
        aliases = Alias.objects.all()
        existing_alias_value = Alias.objects.get(alias='alias')
        self.assertTrue(alias in aliases)
        self.assertEqual(existing_alias_value.end,
                         datetime.datetime(2020, 5, 17, tzinfo=timezone.utc))
