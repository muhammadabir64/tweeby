# Generated by Django 4.1 on 2022-08-21 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_account_email_visible_alter_account_cover_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email_visible',
            field=models.BooleanField(default=True),
        ),
    ]
