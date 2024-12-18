from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from flashcards.models import FlashcardsIndexPage, Flashcard
from .forms import FlashcardInteractionForm
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)




def flashcard_view(request, username, page_id):
    # Tenta obter o usuário pelo username
    user = get_object_or_404(User, username=username)
    index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)

    # Obtém os flashcards associados à FlashcardsIndexPage
    flashcards = Flashcard.objects.filter(index_page=index_page).order_by('position')
    total_flashcards = flashcards.count()

    if total_flashcards == 0:
        raise Http404("No flashcards available.")

    # Índice do cartão atual
    current_card_index = int(request.session.get('current_card_index', 0))
    if current_card_index >= total_flashcards:
        current_card_index = 0

    if request.method == 'POST':
        # Verifica se o formulário é de interação ou de dificuldade
        if 'difficulty' in request.POST:
            difficulty = request.POST['difficulty']
            card_id = request.POST.get('card_id')

            # Atualiza a dificuldade do flashcard atual
            if difficulty and card_id:
                flashcard = get_object_or_404(Flashcard, id=card_id)
                flashcard.difficulty = difficulty
                flashcard.save()
        else:
            form = FlashcardInteractionForm(request.POST)
            if form.is_valid():
                action = form.cleaned_data['action']
                if action == 'select':  # Ação de seleção de flashcard
                    card_id = form.cleaned_data['card_id']
                    current_card_index = list(flashcards.values_list('id', flat=True)).index(card_id)
                    request.session['flipped'] = False
                elif action == 'next':
                    current_card_index = (current_card_index + 1) % total_flashcards
                    request.session['flipped'] = False
                elif action == 'previous':
                    current_card_index = (current_card_index - 1 + total_flashcards) % total_flashcards
                    request.session['flipped'] = False
                elif action == 'flip':
                    request.session['flipped'] = not request.session.get('flipped', False)

                request.session['current_card_index'] = current_card_index

    # Obter o flashcard atual
    current_flashcard = flashcards[current_card_index]
    flipped = request.session.get('flipped', False)

    # Verificar se o usuário atual é o autor da página
    is_author = request.user == index_page.owner
    print(f"Flashcard ID: {current_flashcard.id}, Media: {current_flashcard.media}")
    print(f"Media URL: {current_flashcard.media.url if current_flashcard.media else 'No media'}")
    return render(request, 'flashcards/flashcards_index_page.html', {
        'page_id': page_id,
        'index_page': index_page,
        'flashcards': flashcards,
        'current_flashcard': current_flashcard,
        'flipped': flipped,
        'is_author': is_author,
        'user': user,
        'current_flashcard_index': current_card_index + 1,  # Índice ajustado para ser 1-based
        'question_media_url': current_flashcard.question_media.url if current_flashcard.question_media else None,
        'answer_media_url': current_flashcard.answer_media.url if current_flashcard.answer_media else None,
    })



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def flashcard_interaction(request, page_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.POST.get('action')
        if not action:
            return JsonResponse({'error': 'No action specified'}, status=400)

        index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)

        # Obtém os flashcards associados à FlashcardsIndexPage
        flashcards = Flashcard.objects.filter(index_page=index_page).order_by('position')
        total_flashcards = flashcards.count()

        if total_flashcards == 0:
            return JsonResponse({'error': 'No flashcards available'}, status=404)

        current_card_index = int(request.session.get('current_card_index', 0))
        flipped = request.session.get('flipped', False)

        if action == 'next':
            current_card_index = (current_card_index + 1) % total_flashcards
            flipped = False
        elif action == 'previous':
            current_card_index = (current_card_index - 1 + total_flashcards) % total_flashcards
            flipped = False
        elif action == 'flip':
            flipped = not flipped
        else:
            return JsonResponse({'error': 'Unknown action'}, status=400)

        request.session['current_card_index'] = current_card_index
        request.session['flipped'] = flipped

        flashcard_ids = list(flashcards.values_list('id', flat=True))
        current_flashcard = flashcards[current_card_index]

        return JsonResponse({
            'id': current_flashcard.id,
            'question': current_flashcard.question,
            'answer': current_flashcard.answer,
            'flipped': flipped,
            'index': current_card_index + 1,
            'total': total_flashcards,
            'difficulty': current_flashcard.difficulty,
            'question_media_url': current_flashcard.question_media.url if current_flashcard.question_media else None,
            'answer_media_url': current_flashcard.answer_media.url if current_flashcard.answer_media else None,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def flashcards_list(request, page_id):
    # Verifica se a requisição é GET e AJAX
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Obtém todos os flashcards
        index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)

        # Obtém os flashcards associados à FlashcardsIndexPage
        flashcards = Flashcard.objects.filter(index_page=index_page).order_by('position')
        if not flashcards.exists():
            return JsonResponse({'error': 'No flashcards available'}, status=404)

        # Converte os flashcards em uma lista de dicionários com índice
        flashcards_data = [
            {
                'id': flashcard.id,
                'question': flashcard.question,
                'difficulty': flashcard.difficulty or 'no-difficulty',
                'index': index + 1  # Baseado em 1 para simular forloop.counter
            }
            for index, flashcard in enumerate(flashcards)
        ]

        # Retorna os dados como JSON
        return JsonResponse(flashcards_data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)




@csrf_exempt
def select_flashcard(request, page_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        card_id = request.POST.get('card_id')

        if not card_id:
            return JsonResponse({'error': 'No card_id provided'}, status=400)

        try:
            index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)

            # Obtém os flashcards associados à FlashcardsIndexPage
            flashcards = Flashcard.objects.filter(index_page=index_page).order_by('position')
            flashcard = flashcards.get(id=card_id)

            # Calcule o índice real do flashcard na lista
            flashcard_ids = list(flashcards.values_list('id', flat=True))
            current_card_index = flashcard_ids.index(flashcard.id)

            # Atualiza a sessão
            request.session['current_card_index'] = current_card_index
            request.session['flipped'] = False
            current_flashcard = flashcards[current_card_index]

            return JsonResponse({
                'id': flashcard.id,
                'question': flashcard.question,
                'answer': flashcard.answer,
                'difficulty': flashcard.difficulty,
                'index': current_card_index + 1,  # Exibição baseada em 1
                'question_media_url': current_flashcard.question_media.url if current_flashcard.question_media else None,
                'answer_media_url': current_flashcard.answer_media.url if current_flashcard.answer_media else None,

            })
        except Flashcard.DoesNotExist:
            return JsonResponse({'error': 'Flashcard not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Flashcard ID not in list'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_current_flashcard(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        flashcards = Flashcard.objects.all()
        if not flashcards.exists():
            return JsonResponse({'error': 'No flashcards available'}, status=404)

        current_card_index = request.session.get('current_card_index', 0)
        flipped = request.session.get('flipped', False)

        try:
            current_flashcard = flashcards[current_card_index]
            return JsonResponse({
                'id': current_flashcard.id,
                'question': current_flashcard.question,
                'answer': current_flashcard.answer,
                'flipped': flipped,
                'difficulty': current_flashcard.difficulty,
                'question_media_url': current_flashcard.question_media.url if current_flashcard.question_media else None,
                'answer_media_url': current_flashcard.answer_media.url if current_flashcard.answer_media else None,
            })
        except IndexError:
            return JsonResponse({'error': 'Invalid flashcard index'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def assign_difficulty(request, page_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        difficulty = request.POST.get('difficulty')
        card_id = request.POST.get('card_id')

        if not card_id or not difficulty:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        try:
            # Filtra apenas os flashcards associados ao page_id
            flashcard = Flashcard.objects.get(id=card_id, index_page_id=page_id)
            flashcard.difficulty = difficulty
            flashcard.save()

            # Calcula o índice do flashcard considerando apenas os flashcards do mesmo page_id
            index = Flashcard.objects.filter(index_page_id=page_id, id__lte=flashcard.id).order_by('id').count()

            return JsonResponse({
                'success': True,
                'difficulty': flashcard.difficulty,
                'card_id': flashcard.id,
                'question': flashcard.question,
                'answer': flashcard.answer,
                'index': index,
            })
        except Flashcard.DoesNotExist:
            return JsonResponse({'error': 'Flashcard not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def flashcards_difficulty_count(request, page_id):
    """
    Retorna o número de flashcards por dificuldade como JSON.
    """
    index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)
    counts = index_page.flashcards_count_by_difficulty()  # Presume que essa função já existe no modelo.

    # Certifique-se de retornar valores padrão caso algum contador esteja ausente.
    response_data = {
        'easy': counts.get('easy', 0),
        'medium': counts.get('medium', 0),
        'difficult': counts.get('difficult', 0),
    }

    return JsonResponse(response_data)


from django.utils.text import slugify
from django.urls import reverse
from wagtail.models import Site

from wagtail.models import Site
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify
from .models import FlashcardsIndexPage, Flashcard
from django.core.cache import cache
from django.contrib import messages






def copy_flashcards_index(request, page_id):
    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to clone flashcards.")
        return redirect(reverse('account_login'))

    # Impedir requisições consecutivas (throttling)
    throttle_key = f"copy_flashcards_{request.user.id}_{page_id}"
    throttle_time = 30  # 30 segundos

    if cache.get(throttle_key):
        messages.warning(request, "Please wait before cloning again.")
        return redirect(reverse('wagtailadmin_home'))

    # Define o throttle
    cache.set(throttle_key, True, timeout=throttle_time)

    # Obtém a FlashcardsIndexPage pelo ID
    index_page = get_object_or_404(FlashcardsIndexPage, id=page_id)

    # Verifica se o usuário já possui uma cópia
    base_slug = f"copy-of-{slugify(index_page.slug)}-{request.user.username}"
    parent_page = index_page.get_parent()

    if parent_page.get_children().filter(slug__startswith=base_slug, owner=request.user).exists():
        messages.info(request, "You already have a copy of this deck.")
        return redirect(reverse('flashcard_view', args=(request.user.username, page_id)))

    # Gera um slug único
    unique_slug = base_slug
    counter = 1
    while parent_page.get_children().filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    # Cria uma cópia da página e associa ao usuário logado
    new_index_page = FlashcardsIndexPage(
        title=f"Copy of {index_page.title}",
        slug=unique_slug,
        prompt=index_page.prompt,
        owner=request.user,  # Atribui o proprietário ao usuário autenticado
    )
    parent_page.add_child(instance=new_index_page)

    # Publica a nova página
    new_index_page.save_revision().publish()

    # Copia os flashcards associados
    for flashcard in index_page.get_flashcards():
        new_flashcard = Flashcard(
            question=flashcard.question,
            answer=flashcard.answer,
            difficulty=flashcard.difficulty,
            index_page=new_index_page,  # Associa ao novo FlashcardsIndexPage
        )
        new_flashcard.save()

    # Mensagem de sucesso e redirecionamento
    messages.success(request, f"Deck '{new_index_page.title}' successfully copied!")
    return redirect("flashcard_view", username=request.user.username, page_id=new_index_page.id)







import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def import_flashcards(request, page_id):
    if request.method == 'POST':
        try:
            index_page = FlashcardsIndexPage.objects.get(id=page_id)
            data = json.loads(request.body)

            created_flashcards = []
            for entry in data:
                if "::" in entry:
                    question, answer = entry.split("::", 1)
                    flashcard = Flashcard.objects.create(
                        question=question.strip(),
                        answer=answer.strip(),
                        index_page=index_page
                    )
                    created_flashcards.append({
                        "question": flashcard.question,
                        "answer": flashcard.answer,
                    })

            return JsonResponse({
                "status": "success",
                "created_flashcards": created_flashcards,
            }, status=201)

        except FlashcardsIndexPage.DoesNotExist:
            return JsonResponse({"status": "error", "message": "FlashcardsIndexPage not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

