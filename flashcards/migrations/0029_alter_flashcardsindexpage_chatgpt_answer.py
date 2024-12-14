# Generated by Django 5.1.3 on 2024-12-13 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0028_folderpage_category_folderpage_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcardsindexpage',
            name='chatgpt_answer',
            field=models.TextField(blank=True, help_text='Use the following prompt: "Transform the content below into flashcards in the format Question::Answer (one per line, without enumeration), where the questions are based on the key concepts from the text, according to the guidelines of SuperMemo by Piotr Wozniak. The text and the flashcards must be kept in the same language in which the content was provided."', verbose_name='Paste here the answer from your favorite LLM'),
        ),
    ]
