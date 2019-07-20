# Generated by Django 2.2.1 on 2019-06-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=100, verbose_name='form name')),
                ('form_field', models.TextField(blank=True, null=True, verbose_name='form_field')),
                ('revision', models.IntegerField(blank=True, verbose_name='revision id')),
            ],
        ),
    ]
