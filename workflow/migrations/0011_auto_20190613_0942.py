# Generated by Django 2.2.1 on 2019-06-13 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0010_auto_20190613_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowcondition',
            name='actions',
            field=models.CharField(max_length=500, null=True, verbose_name='Actions'),
        ),
    ]
