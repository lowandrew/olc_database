# Generated by Django 2.0.4 on 2018-04-23 15:31

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_wrapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_terms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_attributes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_operations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_combine_operations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
