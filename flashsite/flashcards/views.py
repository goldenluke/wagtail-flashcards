from django.shortcuts import render
from wagtail.models import Page
from flashcards.models import FlashcardPage
import logging

logger = logging.getLogger(__name__)

def flashcards_view(request):
    try:
        parent_page = Page.objects.get(slug="flashcards")
        logger.info(f"Parent page found: {parent_page.title}")
        flashcards = parent_page.get_children().type(FlashcardPage).live().public()
        logger.info(f"Flashcards found: {flashcards.count()}")
    except Exception as e:
        logger.error(f"Error fetching flashcards: {e}")
        flashcards = FlashcardPage.objects.none()

    return render(request, 'flashcards/flashcards.html', {'flashcards': flashcards})
