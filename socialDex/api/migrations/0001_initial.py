# Generated by Django 3.1.7 on 2021-03-17 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('title', models.CharField(default=None, max_length=120)),
                ('composition', models.TextField()),
                ('address', models.CharField(default=None, max_length=66, null=True)),
                ('hash', models.CharField(default=None, max_length=32, null=True)),
                ('txId', models.CharField(default=None, max_length=66, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
