from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class FlashcardPage(Page):
    question = RichTextField(blank=False)
    answer = RichTextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
