from django.db import models, transaction

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.admin.panels import MultiFieldPanel
from django.utils.text import slugify
from .forms import NoTitleForm
from django.shortcuts import redirect
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from django.shortcuts import render
from wagtail.snippets.models import register_snippet

class RootPage(Page):
    """
    Modelo de página raiz vazio. Serve apenas como um contêiner inicial para subpáginas.
    """
    subpage_types = ['flashcards.FolderPage', 'flashcards.FlashcardsIndexPage', 'flashcards.Box']  # Tipos de subpáginas permitidas
    parent_page_types = []  # Deve ser a raiz, não pode ter pais

    # Nenhum conteúdo ou template necessário
    class Meta:
        verbose_name = "Root"
        verbose_name_plural = "Root"



class Box(Page):
    """
    Modelo que representa a página inicial (Box).
    """
    subpage_types = ['flashcards.FolderPage', 'flashcards.FlashcardsIndexPage']
    parent_page_types = ['flashcards.RootPage']

    def serve(self, request):
        """
        Restringe o acesso ao `Box` para apenas o `owner`.
        """
        if self.owner != request.user:
            return redirect('wagtailadmin_home')
        return super().serve(request)

    class Meta:
        verbose_name = "Folders"
        verbose_name_plural = "Folders"


class FolderPage(Page):
    """
    Uma página simples para organizar FlashcardsIndexPage em pastas.
    """
    subpage_types = ['flashcards.FlashcardsIndexPage', 'flashcards.FolderPage']  # Use o caminho completo para evitar erros
    parent_page_types = ['flashcards.Box']

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"


class Flashcard(Orderable):
    # Relaciona cada Flashcard a um FlashcardsIndexPage
    index_page = ParentalKey(
        'FlashcardsIndexPage',
        on_delete=models.CASCADE,
        related_name='flashcards',  # Nome da relação, usado no InlinePanel
    )
    question = models.TextField(blank=False)
    question_media = models.FileField(upload_to='flashcards_media/questions/', null=True, blank=True)  # Novo campo
    answer = models.TextField(blank=False)
    answer_media = models.FileField(upload_to='flashcards_media/answers/', null=True, blank=True)  # Novo campo
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        blank=True,
    )
    media = models.FileField(upload_to='flashcards_media/', null=True, blank=True)  # Novo campo
    position = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('question'),
        FieldPanel('question_media', classname='question_media'),
        FieldPanel('answer'),
        FieldPanel('answer_media', classname='answer_media'),
        FieldPanel('difficulty'),
    ]

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.question[:50]


from wagtail.admin.viewsets.model import ModelViewSet

class FlashcardViewSet(ModelViewSet):
    model = Flashcard
    menu_label = "Flashcards"
    menu_icon = "form"  # Altere para qualquer ícone do Wagtail
    menu_order = 300
    add_to_admin_menu = True
    list_display = ("question", "difficulty")
    search_fields = ("question", "answer")

from wagtail.search import index

class FlashcardsIndexPage(Page):
    """A page that acts as an index for flashcards."""

    # Optional description or introduction for the index page
    prompt = models.TextField(blank=True, help_text="Text to describe the flashcards.")
    chatgpt_answer = models.TextField(
        blank=True,
        help_text="Paste the array of flashcards in the format: 'question::answer' (one per line).",
    )
    category = models.CharField(max_length=100, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('prompt'),
        FieldPanel('chatgpt_answer'),
        InlinePanel('flashcards', label="Flashcards"),
    ]

    search_fields = Page.search_fields + [
    index.SearchField('title'),
    index.FilterField('owner'),
    index.FilterField('category'),
    ]


    def get_flashcards(self):
        # Retorna todos os flashcards associados a esta página
        return self.flashcards.order_by('position')

    def serve(self, request):
        # Determinar o índice atual do flashcard
        current_card_index = int(request.session.get('current_card_index', 0))
        flipped = request.session.get('flipped', False)
        username = self.owner.username  # Obtém o nome de usuário do dono da página
        if request.path != f"/{username}/{self.id}/":
            return redirect("flashcard_view", username=username, page_id=self.id)


        # Obter flashcards associados
        flashcards = self.get_flashcards()
        is_author = request.user == self.owner
        # Processar ações do formulário
        if request.method == "POST":
            action = request.POST.get("action")

            # Processar dificuldade
            if "difficulty" in request.POST:
                card_id = request.POST.get("card_id")
                difficulty = request.POST.get("difficulty")
                try:
                    flashcard = flashcards.get(id=card_id)
                    flashcard.difficulty = difficulty
                    flashcard.save()
                except Flashcard.DoesNotExist:
                    pass

            # Processar ações de navegação e flip
            elif action == "previous":
                current_card_index = (current_card_index - 1 + flashcards.count()) % flashcards.count()
                flipped = False  # Reseta o estado de flip ao navegar
            elif action == "next":
                current_card_index = (current_card_index + 1) % flashcards.count()
                flipped = False  # Reseta o estado de flip ao navegar
            elif action == "flip":
                flipped = not flipped  # Alterna o estado de flip

            # Processar seleção de flashcard
            elif action == "select":
                card_id = request.POST.get("card_id")
                try:
                    selected_flashcard = flashcards.get(id=card_id)
                    current_card_index = list(flashcards.values_list("id", flat=True)).index(selected_flashcard.id)
                    flipped = False  # Reseta o estado de flip ao selecionar
                except Flashcard.DoesNotExist:
                    pass

            # Salvar estado na sessão
            request.session['current_card_index'] = current_card_index
            request.session['flipped'] = flipped

        # Determinar o flashcard atual
        current_card_index = int(request.session.get('current_card_index', 0))
        current_flashcard = flashcards[current_card_index] if flashcards.exists() else None


        # Passar contexto ao template
        return render(request, "flashcards/flashcards_index_page.html", {
            "index_page": self,
            "flashcards": flashcards,
            "current_flashcard": current_flashcard,
            "flipped": flipped,
            "is_author": is_author,
        })
    class Meta:
        verbose_name = "Deck"
        verbose_name_plural = "Decks"


    def save(self, *args, **kwargs):
        """Override save to process chatgpt_answer."""
        super().save(*args, **kwargs)

        if self.chatgpt_answer:
            lines = self.chatgpt_answer.splitlines()

            # Verifica perguntas já existentes
            existing_questions = set(
                Flashcard.objects.filter(index_page=self).values_list('question', flat=True)
            )

            flashcards_to_create = []
            for line in lines:
                if "::" in line:
                    question, answer = map(str.strip, line.split("::", 1))
                    if question not in existing_questions:
                        flashcards_to_create.append(
                            Flashcard(question=question, answer=answer, index_page=self)
                        )

            # Cria flashcards em massa
            Flashcard.objects.bulk_create(flashcards_to_create)









    def copy_page(self, user):
        """Copy this FlashcardsIndexPage and its FlashcardPage children for a user."""
        username = user.username if user and user.is_authenticated else "guest"
        base_slug = f"copy-of-{self.slug}-{username}"
        new_slug = base_slug
        parent_page = self.get_parent()

        # Garante que o slug seja único
        counter = 1
        while parent_page.get_children().filter(slug=new_slug).exists():
            new_slug = f"{base_slug}-{counter}"
            counter += 1

        # Cria uma nova FlashcardsIndexPage
        new_index_page = FlashcardsIndexPage(
            title=f"Copy of {self.title}",
            slug=new_slug,
            prompt=self.prompt,
        )
        new_index_page.owner = user if user and user.is_authenticated else None  # Atribui o owner
        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()

        # Copia os FlashcardPage associados
        for flashcard in self.get_flashcards():
            flashcard_slug_base = f"copy-of-{flashcard.slug}-{username}"
            flashcard_slug = flashcard_slug_base

            # Garante que o slug dos flashcards seja único
            counter = 1
            while new_index_page.get_children().filter(slug=flashcard_slug).exists():
                flashcard_slug = f"{flashcard_slug_base}-{counter}"
                counter += 1

            new_flashcard = FlashcardPage(
                title=flashcard.title,
                slug=flashcard_slug,
                question=flashcard.question,
                answer=flashcard.answer,
                difficulty=flashcard.difficulty,
            )
            new_flashcard.owner = user if user and user.is_authenticated else None  # Atribui o owner
            new_index_page.add_child(instance=new_flashcard)
            new_flashcard.save_revision().publish()

        return new_index_page


