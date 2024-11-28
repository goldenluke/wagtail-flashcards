# Generated by Django 5.1.3 on 2024-11-28 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0011_remove_flashcard_answer_media_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='answer_media',
            field=models.FileField(blank=True, null=True, upload_to='flashcards_media/answers/'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='question_media',
            field=models.FileField(blank=True, null=True, upload_to='flashcards_media/questions/'),
        ),
    ]
