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


@hooks.register('construct_main_menu')
def hide_help_and_reports_menu_items(request, menu_items):
    # Filter out Help and Reports menu items by their name or URL
    menu_items[:] = [
        item for item in menu_items
        if item.name not in ['help', 'reports']
    ]


from wagtail.models import Page

@hooks.register("construct_explorer_page_queryset")
def restrict_pages_to_owner(parent_page, pages, request):
    """
    Restringe a visualização de páginas apenas ao dono no explorador de páginas.
    """
    if request.user.is_superuser:
        return pages  # Superusuários podem ver todas as páginas

    # Filtra apenas as páginas onde o usuário logado é o proprietário
    return pages.filter(owner=request.user)


from wagtail import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('construct_main_menu')
def change_pages_menu(request, menu_items):
    for item in menu_items:
        if item.name == 'explorer':  # Identifica o menu "Pages"
            item.label = "Folders"  # Substitua "Decks" pelo nome desejado







@hooks.register('insert_editor_js')
def add_custom_admin_js():
    return """
        <script src="/static/flashcards/js/admin.js"></script>
    """



from wagtail import hooks
from wagtail.models import Page

@hooks.register('construct_explorer_page_queryset')
def filter_box_queryset(parent_page, pages, request):
    """
    Filtra os Boxes para exibir apenas os pertencentes ao usuário logado.
    """
    if request.user.is_superuser:
        return pages  # Administradores podem ver todos os Boxes

    # Filtra para que o usuário veja apenas os Boxes que ele possui
    return pages.filter(owner=request.user)

