# Generated by Django 5.1.3 on 2024-11-25 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0005_flashcardsindexpage_cloned_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcardsindexpage',
            name='cloned_by',
        ),
    ]