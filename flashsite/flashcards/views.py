from django.shortcuts import render, get_object_or_404
from django.http import Http404
from flashcards.models import FlashcardPage
from .forms import FlashcardInteractionForm
import logging

logger = logging.getLogger(__name__)


def flashcard_view(request, page_id):
    # Tenta obter os flashcards publicados
    flashcards = FlashcardPage.objects.filter(live=True).order_by('id')
    total_flashcards = flashcards.count()

    if total_flashcards == 0:
        raise Http404("No flashcards available.")

    # Índice do cartão atual
    current_card_index = int(request.session.get('current_card_index', 0))

    # Certifique-se de que o índice atual esteja dentro do intervalo
    if current_card_index >= total_flashcards:
        current_card_index = 0

    if request.method == 'POST':
        form = FlashcardInteractionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            if action == 'select':  # Ação de seleção de flashcard
                card_id = form.cleaned_data['card_id']
                selected_flashcard = get_object_or_404(FlashcardPage, id=card_id)
                current_card_index = list(flashcards.values_list('id', flat=True)).index(card_id)
                request.session['current_card_index'] = current_card_index
            elif action == 'next':
                current_card_index = (current_card_index + 1) % total_flashcards
            elif action == 'previous':
                current_card_index = (current_card_index - 1 + total_flashcards) % total_flashcards
            elif action == 'flip':
                request.session['flipped'] = not request.session.get('flipped', False)

            difficulty = form.cleaned_data.get('difficulty')
            if difficulty:
                card_id = form.cleaned_data['card_id']
                try:
                    flashcard = get_object_or_404(FlashcardPage, id=card_id)
                    flashcard.difficulty = difficulty
                    flashcard.save()
                except Http404:
                    logger.warning(f"Flashcard ID {card_id} not found for difficulty update.")

            request.session['current_card_index'] = current_card_index

    # Obter o flashcard atual
    current_flashcard = flashcards[current_card_index]
    flipped = request.session.get('flipped', False)

    return render(request, 'flashcards/flashcard.html', {
        'flashcards': flashcards,
        'current_flashcard': current_flashcard,
        'flipped': flipped,
        'form': FlashcardInteractionForm(initial={'card_id': current_flashcard.id}),
    })
