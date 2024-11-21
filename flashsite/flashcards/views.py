from django.shortcuts import render

from .models import FlashcardPage

def flashcards_view(request):
    flashcards = FlashcardPage.objects.live().public()
    return render(request, 'flashcards/flashcards.html', {'flashcards': flashcards})
