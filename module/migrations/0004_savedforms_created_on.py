# Generated by Django 2.2.1 on 2019-06-18 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_savedforms_status_wrkflw'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedforms',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created on'),
            preserve_default=False,
        ),
    ]
