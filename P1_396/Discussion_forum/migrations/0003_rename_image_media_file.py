# Generated by Django 4.1.1 on 2022-09-25 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion_forum', '0002_alter_media_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='image',
            new_name='file',
        ),
    ]
