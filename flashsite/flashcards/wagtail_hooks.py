from wagtail.admin.action_menu import ActionMenuItem
from wagtail import hooks
from django.urls import reverse
from flashcards.models import FlashcardsIndexPage, Flashcard
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.menu import SubmenuMenuItem, MenuItem
from wagtail.models import Page


class CloneFlashcardsMenuItem(ActionMenuItem):
    name = "action-clone-flashcards"
    label = "Clone This Flashcards Index"

    def is_shown(self, context):
        # Check if the page is of the correct type and belongs to another user
        page = context.get("page", None)
        request = context.get("request", None)
        if page and isinstance(page.specific, FlashcardsIndexPage):
            return page.owner != request.user
        return False

    def get_url(self, context):
        page = context["page"]
        return reverse("copy_flashcards_index", args=[page.id])


from .models import Flashcard

class FlashcardViewSet(ModelViewSet):
    model = Flashcard
    menu_label = "Flashcards"
    menu_icon = "form"  # Escolha o ícone adequado (https://fontawesome.com/icons)
    menu_order = 300
    add_to_admin_menu = True
    list_display = ("question", "difficulty")
    search_fields = ("question", "answer")

@hooks.register("register_admin_viewset")
def register_flashcard_viewset():
    return FlashcardViewSet("flashcards")


from wagtail import hooks
from django.utils.html import format_html



@hooks.register('construct_page_edit_handler')
def customize_flashcard_edit_handler(handler, request, context):
    if hasattr(context['instance'], 'question_media'):
        context['media_thumbnails_template'] = 'wagtailadmin/pages/edit_flashcard.html'



@hooks.register('insert_editor_js')
def add_custom_admin_js():
    return """
        <script src="/static/flashcards/js/admin.js"></script>
    """




