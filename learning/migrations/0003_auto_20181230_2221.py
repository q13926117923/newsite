# Generated by Django 2.1.2 on 2018-12-30 14:21

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20181219_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]