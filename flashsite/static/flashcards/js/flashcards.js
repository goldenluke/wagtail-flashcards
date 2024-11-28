document.addEventListener('DOMContentLoaded', () => {
    const sidePanelList = document.getElementById('flashcards-list'); // Lista no side-panel
    const flashcardElement = document.getElementById('flashcard'); // Flashcard principal
    const questionCardElement = document.querySelector('.card-blue'); // Lado da pergunta
    const answerCardElement = document.querySelector('.card-red'); // Lado da resposta
    const questionElement = document.querySelector('.card-blue p');
    const answerElement = document.querySelector('.card-red p');
    const selectedFlashcardContainer = document.getElementById('selected-flashcard'); // Flashcard selecionado
    const difficultyButtons = document.querySelectorAll('#difficulty-container button'); // Botões de dificuldade
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const selectedFlashcardElement = document.getElementById('selected-flashcard');
    const flashcardsList = document.querySelectorAll('flashcards-list'); // Lista de flashcards







    const sendAction = async (action) => {
        try {
            const response = await fetch('/flashcards/interaction/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'x-requested-with': 'XMLHttpRequest',
                },
                body: new URLSearchParams({ action }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Action processed:', action, data);

                if (action === 'flip') {
                    toggleFlashcard(data.flipped);
                } else {
                    updateFlashcard(data);
                    updateSelectedFlashcard(data); // Atualizar o flashcard selecionado
                    updateFlashcardsListStyle(data.id, data.difficulty);
                    updateDifficultyButtons(data.difficulty);
                    console.log('Data received from backend:', data);

                    // Recarregar a lista de flashcards
                    await reloadFlashcardsList(data.id)
                }
            } else {
                console.error('Failed to process action:', action);
            }


        } catch (error) {
            console.error('Error:', error);
        }
    };










    const toggleFlashcard = (flipped) => {
        if (flipped) {
            questionCardElement.style.display = 'none';
            answerCardElement.style.display = 'block';
        } else {
            questionCardElement.style.display = 'block';
            answerCardElement.style.display = 'none';
        }
    };

    const updateFlashcardsList = (currentIndex) => {
        flashcardsList.forEach((li, index) => {
            // currentIndex - 1 porque o índice do backend é baseado em 1
            if (index === currentIndex - 1) {
                li.classList.add('selected');
            } else {
                li.classList.remove('selected');
            }
        });
    };


    // Evento para o botão Flip
    document.getElementById('flip-button').addEventListener('click', (event) => {
        event.preventDefault();
        sendAction('flip');
    });

    // Evento para o botão Next
    document.getElementById('next-button').addEventListener('click', (event) => {
        event.preventDefault();
        sendAction('next');
    });

    // Evento para o botão Previous
    document.getElementById('previous-button').addEventListener('click', (event) => {
        event.preventDefault();
        sendAction('previous');
    });

    // Evento para o Flashcard (Flip ao clicar no card)
    flashcardElement.addEventListener('click', (event) => {
        event.preventDefault();
        sendAction('flip'); // Chama a ação de flip
    });












    // Carregar a lista de flashcards dinamicamente
    const loadFlashcardsList = async () => {
        try {
            const response = await fetch('/flashcards/list/', {
                method: 'GET',
                headers: {
                    'x-requested-with': 'XMLHttpRequest',
                },
            });

            if (response.ok) {
                const flashcards = await response.json();

                // Limpa a lista antes de preenchê-la
                sidePanelList.innerHTML = '';

                // Adiciona os flashcards na lista
                flashcards.forEach((flashcard, index) => {
                    const listItem = document.createElement('li');
                    listItem.className = flashcard.difficulty || 'no-difficulty'; // Classe de dificuldade
                    listItem.innerHTML = `
                        <a href="#" data-id="${flashcard.id}" data-index="${index}">
                            Card ${index + 1}: ${flashcard.question.slice(0, 50)}${flashcard.question.length > 50 ? '...' : ''}
                        </a>
                    `;
                    listItem.addEventListener('click', (event) => selectFlashcard(event, flashcard.id));
                    sidePanelList.appendChild(listItem);
                });

                console.log('Flashcards loaded successfully:', flashcards);
            } else {
                console.error('Failed to load flashcards list.');
            }
        } catch (error) {
            console.error('Error loading flashcards list:', error);
        }
    };




    // Atualizar flashcard no painel principal
    const updateFlashcard = (flashcard) => {
        questionElement.textContent = flashcard.question;
        answerElement.textContent = flashcard.answer;

        // Reseta para mostrar a pergunta
        questionCardElement.style.display = 'block';
        answerCardElement.style.display = 'none';

        console.log('Flashcard updated:', flashcard);
    };



    const selectFlashcard = async (event, flashcardId) => {
        event.preventDefault();

        if (!Number.isInteger(flashcardId)) {
            console.error(`Invalid flashcard ID: ${flashcardId}`);
            return;
        }

        try {
            const response = await fetch('/flashcards/select/', {
                method: 'POST',
                headers: {
                    'x-requested-with': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    card_id: flashcardId,
                }),
            });

            if (response.ok) {
                const data = await response.json();

                // Atualiza o flashcard principal
                updateFlashcard(data);

                // Atualiza os botões de dificuldade
                updateDifficultyButtons(data.difficulty);

                // Marca o item correspondente na lista como "selected"
                updateFlashcardsListStyle(data.id, data.difficulty);

                // Atualiza o flashcard selecionado
                updateSelectedFlashcard(data);

                console.log('Flashcard selected:', data);
            } else {
                console.error('Failed to select flashcard:', await response.text());
            }
        } catch (error) {
            console.error('Error selecting flashcard:', error);
        }
    };

    window.selectFlashcard = selectFlashcard;




    // Carrega a lista de flashcards ao carregar a página
    loadFlashcardsList();




const updateDifficultyButtons = (difficulty) => {
    const buttons = document.querySelectorAll('#difficulty-container button');

    buttons.forEach((button) => {
        // Remove destaque de todos os botões
        button.classList.remove('highlight');

        // Adiciona destaque ao botão correspondente
        if (button.name === 'difficulty' && button.value === difficulty) {
            button.classList.add('highlight');
        }
    });

    console.log('Difficulty buttons updated:', difficulty);
};



const updateFlashcardsListStyle = (cardId, difficulty) => {
    // Seleciona todos os itens da lista
    const flashcardItems = document.querySelectorAll('#flashcards-list li');

    flashcardItems.forEach((item) => {
        const id = item.getAttribute('data-id');

        // Verifica se o item tem um ID correspondente
        if (id === String(cardId)) {
            // Aplica a classe "selected" ao item correspondente
            item.classList.add('selected');
            item.classList.remove('easy', 'medium', 'hard', 'no-difficulty'); // Remove todas as classes de dificuldade
            item.classList.add(difficulty || 'no-difficulty'); // Adiciona a nova dificuldade
            console.log(`Updated flashcard ID: ${cardId} to difficulty: ${difficulty} and marked as selected.`);
        } else {
            // Remove a classe "selected" de outros itens
            item.classList.remove('selected');
        }
    });
};






const updateSelectedFlashcard = (data) => {
    const selectedFlashcardElement = document.getElementById('selected-flashcard');

    if (selectedFlashcardElement) {
        selectedFlashcardElement.className = data.difficulty || 'no-difficulty'; // Classe de dificuldade

        selectedFlashcardElement.innerHTML = `
            <p>
                Card ${data.index}:
                ${data.question.slice(0, 50)}${data.question.length > 50 ? '...' : ''}
            </p>
        `;
    }

    console.log('Selected flashcard updated:', data);
};


const reloadFlashcardsList = async (currentCardId = null) => {
    try {
        const response = await fetch('/flashcards/list/', {
            method: 'GET',
            headers: {
                'x-requested-with': 'XMLHttpRequest',
            },
        });

        if (response.ok) {
            const data = await response.json();
            const flashcardsList = document.getElementById('flashcards-list');

            if (!flashcardsList) {
                console.error('Flashcards list container not found.');
                return;
            }

            // Reconstrói a lista de flashcards
            flashcardsList.innerHTML = data.map(flashcard => `
            <li data-id="${flashcard.id}"
            class="${flashcard.difficulty} ${flashcard.id === currentCardId ? 'selected' : ''}">
            <a href="#" onclick="selectFlashcard(event, ${flashcard.id}); return false;">
            Card ${flashcard.index}: ${flashcard.question.slice(0, 50)}${flashcard.question.length > 50 ? '...' : ''}
            </a>
            </li>
            `).join('');

            console.log('Flashcards list reloaded successfully.');

            // Restaura o elemento `selectedFlashcardElement`
            if (currentCardId) {
                const currentItem = flashcardsList.querySelector(`li[data-id="${currentCardId}"]`);
                if (currentItem) {
                    currentItem.classList.add('selected');
                    const selectedFlashcardElement = document.getElementById('selected-flashcard');
                    selectedFlashcardElement.dataset.id = currentCardId;
                }
            }
        } else {
            console.error('Failed to reload flashcards list.');
        }
    } catch (error) {
        console.error('Error reloading flashcards list:', error);
    }
};











const assignDifficulty = async (difficulty) => {
    const selectedFlashcardElement = document.getElementById('selected-flashcard');
    const cardId = selectedFlashcardElement ? selectedFlashcardElement.dataset.id : null;

    if (!cardId) {
        console.error('Flashcard ID is undefined. Cannot assign difficulty.');
        return;
    }

    console.log(`Assigning difficulty "${difficulty}" to card ID: ${cardId}`);

    try {
        const payload = new URLSearchParams({
            difficulty: difficulty.trim(),
                                            card_id: String(cardId).trim(),
        });

        console.log('Payload:', payload.toString());

        const response = await fetch('/flashcards/difficulty/', {
            method: 'POST',
            headers: {
                'x-requested-with': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: payload,
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Difficulty assigned successfully:', data);

            // Recarrega a lista preservando o flashcard selecionado
            await reloadFlashcardsList(data.card_id);

            // Atualiza o flashcard selecionado
            updateSelectedFlashcard(data);
        } else {
            const errorText = await response.text();
            console.error('Failed to assign difficulty:', errorText);
        }
    } catch (error) {
        console.error('Error assigning difficulty:', error);
    }
};















    // Adiciona evento de clique aos botões de dificuldade
    difficultyButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o envio do formulário padrão

            const difficulty = button.value;

            // Atualiza a interface imediatamente
            updateDifficultyButtons(difficulty);

            // Faz a requisição para atualizar no backend
            assignDifficulty(difficulty);
        });
    });
});





function toggleSidePanel() {
    const sidePanel = document.getElementById('side-panel');
    const mainContainer = document.getElementById('main-container');
    const openButton = document.querySelector('.open-btn');
    const closeButton = document.querySelector('.close-btn');

    if (sidePanel) {
        sidePanel.classList.toggle('open'); // Alterna a classe "open"

        if (sidePanel.classList.contains('open')) {
            openButton.style.display = 'none'; // Oculta o botão "☰ Menu"
            closeButton.style.display = 'block'; // Exibe o botão "×"
            mainContainer.style.marginLeft = '300px'; // Adiciona o deslocamento
        } else {
            openButton.style.display = 'block'; // Exibe o botão "☰ Menu"
            closeButton.style.display = 'none'; // Oculta o botão "×"
            mainContainer.style.marginLeft = '0'; // Remove o deslocamento
        }
    }
}




