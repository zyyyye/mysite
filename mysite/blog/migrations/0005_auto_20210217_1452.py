# Generated by Django 3.1.6 on 2021-02-17 14:52

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210207_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
