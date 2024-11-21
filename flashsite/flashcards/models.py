from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import MultiFieldPanel
from django.utils.text import slugify
from .forms import NoTitleForm

class FlashcardPage(Page):
    question = models.TextField(blank=False)
    answer = models.TextField(blank=False)

    base_form_class = NoTitleForm

    content_panels =  [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    def full_clean(self, *args, **kwargs):
        # Sincroniza o título com a pergunta antes da validação
        if not self.title and self.question:
            self.title = self.question
        if not self.slug and self.question:
            self.slug = slugify(self.question[:50])

        print(f"Model full_clean: title={self.title}, slug={self.slug}")
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Reforça a sincronização antes de salvar
        if not self.title:
            self.title = self.question
        if not self.slug:
            self.slug = slugify(self.question[:50])

        print(f"Model save: title={self.title}, slug={self.slug}")
        super().save(*args, **kwargs)

    @classmethod
    def allowed_parent_page_models(cls):
        # Apenas FlashcardsIndexPage pode ser pai de FlashcardPage
        from .models import FlashcardsIndexPage
        return [FlashcardsIndexPage]

    @classmethod
    def allowed_subpage_models(cls):
        # Não permite subpáginas
        return []


class FlashcardsIndexPage(Page):
    """A page that acts as an index for flashcards."""

    # Optional description or introduction for the index page
    introduction = models.TextField(blank=True, help_text="Text to describe the flashcards.")

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    @classmethod
    def allowed_subpage_models(cls):
        # Only allow FlashcardPage as child pages
        from .models import FlashcardPage
        return [FlashcardPage]

    def get_flashcards(self):
        # Fetch all child flashcards
        from .models import FlashcardPage
        return self.get_children().live().specific().type(FlashcardPage)

