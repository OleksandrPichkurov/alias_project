from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

import datetime

# Create your models here.


def get_aliases(target, from_date, to_date):
    '''
        Returns a set of aliases for specific target in the specific
        time range(from_date, to_date)

        Examples in manage.py shell:
        from datetime import timedelta
        from django.utils import timezone
        from alias.models import Alias, get_aliases
        import datetime
        a = get_aliases(target='sometarget',
                        from_date=datetime.datetime.now(),
                        to_date=datetime.datetime.max)
    '''
    return Alias.objects.filter(target=target).filter(start__lte=to_date,
                                                      end__gte=from_date)


def alias_replace(existing_alias, replace_at, new_alias_value):
    '''
        Creates the new alias with start field set to replace_at moment

        Examples in manage.py shell:
        from datetime import timedelta
        from django.utils import timezone
        from alias.models import Alias, get_aliases,
                                 alias_update, alias_replace
        a = alias_replace(existing_alias='useful',
                          replace_at=timezone.now(),
                          new_alias_value='one_more_alias')
    '''
    alias_update(existing_alias, replace_at)
    return Alias.objects.create(alias=new_alias_value, start=replace_at)


def alias_update(existing_alias, replace_at):
    '''
        Returns the updated existing aliases, 
        end field set to replace_at moment
    '''
    return Alias.objects.filter(alias=existing_alias).update(end=replace_at)


class Alias(models.Model):
    alias = models.CharField(max_length=255)
    target = models.CharField(max_length=24)
    start = models.DateTimeField()
    # if the end field is not set, the maximum possible date is
    # automatically assigned(continue forever)
    end = models.DateTimeField(blank=True, default=datetime.datetime.max)
    # content_type, object_id, content_object
    # fields for the ability to make relations with other project models
    target_type = models.ForeignKey(ContentType,
                                     blank=True,
                                     null=True,
                                     on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target_object = GenericForeignKey('target_type', 'target_id')

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        '''
            checks if the existing alias with datatime in the
            database overlaps with the new alias with datetime.
            start field is inclusive, end field is exclusive
            If not - save, if yes - raise ValidationError
            Examples in manage.py shell:
            a = Alias.objects.create(alias='new_alias',
                                     target='sometarget',
                                     start=timezone.now()-timedelta(days=50))
        '''
        alias_overlap = Alias.objects.filter(alias=self.alias).filter(
            Q(start__lt=self.end, end__gte=self.start)
            ).exists()
        if alias_overlap:
            raise ValidationError('This alias overlap by time with another \
                                    aliases.')

        return super(Alias, self).save(*args, **kwargs)
