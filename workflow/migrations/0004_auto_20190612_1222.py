# Generated by Django 2.2.1 on 2019-06-12 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_remove_createrule_form_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='conditions',
            field=models.CharField(max_length=50, null=True, verbose_name='Conditions'),
        ),
    ]
