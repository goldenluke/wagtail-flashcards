from wagtail.models import Page
from django.contrib.auth.models import User

def clone_flashcards_index_page(original_page: Page, target_user: User):
    """
    Clona a FlashcardsIndexPage e suas páginas filhas para um novo usuário.
    """
    # Clona a FlashcardsIndexPage
    cloned_index_page = original_page.copy(
        update_attrs={
            "title": f"Clone of {original_page.title}",
            "owner": target_user,
        },
        recursive=False,
    )

    # Clona as FlashcardPages associadas
    for child_page in original_page.get_children().specific():
        child_page.copy(
            to=cloned_index_page,
            update_attrs={
                "owner": target_user,
            },
        )

    return cloned_index_page

@hooks.register('register_admin_menu_item')
def register_flashcards_index_menu():
    return MenuItem(
        'Flashcards Index',
        reverse('wagtailadmin_explore', args=[Page.objects.filter(title="Home").first().id]),
        classnames='icon icon-folder-inverse',
        order=200,
    )
