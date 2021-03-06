# Generated by Django 4.0.1 on 2022-01-21 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название трека', max_length=60)),
                ('track_url', models.CharField(help_text='Ссылка на файл (Firestore Storage)', max_length=256)),
                ('published_by', models.ForeignKey(help_text='Кем опубликовано', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
