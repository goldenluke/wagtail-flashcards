# Generated by Django 5.1.3 on 2024-11-28 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0012_flashcard_answer_media_flashcard_question_media'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flashcard',
            options={'verbose_name': 'Flashcard', 'verbose_name_plural': 'Flashcards'},
        ),
    ]
