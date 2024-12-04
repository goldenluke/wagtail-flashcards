# Generated by Django 5.1.3 on 2024-11-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0010_remove_flashcard_media_flashcard_answer_media_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='answer_media',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='question_media',
        ),
        migrations.AddField(
            model_name='flashcard',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='flashcards_media/'),
        ),
    ]