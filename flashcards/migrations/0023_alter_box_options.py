# Generated by Django 5.1.3 on 2024-12-01 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0022_alter_box_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='box',
            options={'verbose_name': 'Folders', 'verbose_name_plural': 'Folders'},
        ),
    ]
