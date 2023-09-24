# Generated by Django 4.0.6 on 2022-08-05 09:12

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_img', models.URLField(default='https://pbs.twimg.com/profile_images/1543595364460011521/TggWO3m2_400x400.jpg')),
                ('cover_img', models.URLField(default='https://pbs.twimg.com/profile_banners/1524287599216496640/1652255325/1500x500')),
                ('flag', models.CharField(max_length=25)),
                ('country', models.CharField(max_length=125)),
                ('city', models.CharField(max_length=125)),
                ('star_badge', models.BooleanField(default=False)),
                ('thread_code', models.CharField(default='AALD2SMGOR', max_length=125, unique=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='user_followers', to='account.account')),
                ('following', models.ManyToManyField(blank=True, related_name='user_following', to='account.account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
