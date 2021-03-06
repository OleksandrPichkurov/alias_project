# Generated by Django 3.0 on 2021-02-11 09:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=255)),
                ('target', models.CharField(max_length=24)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999))),
                ('target_id', models.PositiveIntegerField(blank=True, null=True)),
                ('target_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
