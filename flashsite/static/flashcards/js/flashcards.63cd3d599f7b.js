document.addEventListener('DOMContentLoaded', async () => {
    const sidePanelList = document.getElementById('flashcards-list'); // Lista no side-panel
    const flashcardElement = document.getElementById('flashcard'); // Flashcard principal
    const questionCardElement = document.querySelector('.card-blue'); // Lado da pergunta
    const answerCardElement = document.querySelector('.card-red'); // Lado da resposta
    const questionElement = document.querySelector('.card-blue p');
    const answerElement = document.querySelector('.card-red p');
    const selectedFlashcardContainer = document.getElementById('selected-flashcard'); // Flashcard selecionado
    const difficultyButtons = document.querySelectorAll('#difficulty-container button'); // Botões de dificuldade
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const questionMedia = document.getElementById('question-media'); // Substitua pelo ID correto
    const answerMedia = document.getElementById('answer-media'); // Substitua pelo ID correto
    const selectedFlashcardElement = document.getElementById('selected-flashcard');
    const flashcardsList = document.querySelectorAll('flashcards-list'); // Lista de flashcards




    const showLoading = () => {
        const loadingIndicator = document.getElementById('loader');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }
    };

    const hideLoading = () => {
        const loadingIndicator = document.getElementById('loader');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    };


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

                // Obtém o ID do flashcard selecionado do localStorage
                const selectedFlashcardId = localStorage.getItem('selectedFlashcard');

                // Adiciona os flashcards na lista
                flashcards.forEach((flashcard, index) => {
                    const isSelected = flashcard.id === parseInt(selectedFlashcardId, 10);

                    const listItem = document.createElement('li');
                    listItem.className = `${flashcard.difficulty || 'no-difficulty'} ${isSelected ? 'selected' : ''}`;
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

                // Fallback to localStorage if currentCardId is null
                const selectedCardId = currentCardId || parseInt(localStorage.getItem('selectedFlashcard'), 10);

                // Rebuild the list
                flashcardsList.innerHTML = ''; // Clear existing items
                data.forEach(flashcard => {
                    const isSelected = flashcard.id === selectedCardId;

                    const listItem = document.createElement('li');
                    listItem.setAttribute('data-id', flashcard.id);
                    listItem.className = `${flashcard.difficulty} ${isSelected ? 'selected' : ''}`;
                    listItem.innerHTML = `
                    <a href="#" onclick="selectFlashcard(event, ${flashcard.id}); return false;">
                    Card ${flashcard.index}: ${flashcard.question.slice(0, 50)}${flashcard.question.length > 50 ? '...' : ''}
                    </a>
                    `;

                    // Attach event listener
                    listItem.querySelector('a').addEventListener('click', (event) =>
                    selectFlashcard(event, flashcard.id)
                    );

                    flashcardsList.appendChild(listItem);
                });

                console.log('Flashcards list reloaded successfully.');
                highlightFlashcardInList(selectedCardId);

                // Update `selectedFlashcardElement`
                const selectedFlashcardElement = document.getElementById('selected-flashcard');
                if (selectedCardId && selectedFlashcardElement) {
                    const selectedFlashcard = data.find(flashcard => flashcard.id === selectedCardId);
                    if (selectedFlashcard) {
                        selectedFlashcardElement.dataset.id = selectedCardId;
                        selectedFlashcardElement.className = selectedFlashcard.difficulty || 'no-difficulty';
                        selectedFlashcardElement.innerHTML = `
                        <p>
                        Card ${selectedFlashcard.index}:
                        ${selectedFlashcard.question.slice(0, 50)}${selectedFlashcard.question.length > 50 ? '...' : ''}
                        </p>
                        `;
                    }
                }

                // Save `currentCardId` to localStorage
                if (selectedCardId) {
                    localStorage.setItem('selectedFlashcard', selectedCardId);
                }
            } else {
                console.error('Failed to reload flashcards list.');
            }
        } catch (error) {
            console.error('Error reloading flashcards list:', error);
        }
    };




    const selectFlashcard = async (event, flashcardId) => {
        event.preventDefault();

        if (!Number.isInteger(flashcardId)) {
            console.error(`Invalid flashcard ID: ${flashcardId}`);
            return;
        }

        try {
            showLoading(); // Exibe o GIF de carregamento

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

                updateMedia(data);

                // Salva no localStorage
                localStorage.setItem('selectedFlashcard', flashcardId);

                console.log('Flashcard selected:', data);
            } else {
                console.error('Failed to select flashcard:', await response.text());
            }
        } catch (error) {
            console.error('Error selecting flashcard:', error);
        } finally {
            hideLoading(); // Esconde o GIF de carregamento
        }
    };

    window.selectFlashcard = selectFlashcard;



    const highlightFlashcardInList = (flashcardId) => {
        const flashcardItems = document.querySelectorAll('#flashcards-list li');

        flashcardItems.forEach((item) => {
            const id = item.getAttribute('data-id');

            if (id === String(flashcardId)) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });

        console.log(`Highlighted flashcard ID: ${flashcardId}`);
    };


    const sendAction = async (action) => {
        try {
            showLoading(); // Exibe o GIF de carregamento

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
                    console.log('Response data from backend:', data);
                    updateMedia(data);
                    updateFlashcard(data);
                    updateSelectedFlashcard(data); // Atualizar o flashcard selecionado
                    updateFlashcardsListStyle(data.id, data.difficulty);
                    updateDifficultyButtons(data.difficulty);
                    console.log('Data received from backend:', data);
                    localStorage.setItem('selectedFlashcard', data.id);

                    // Recarregar a lista de flashcards
                    await reloadFlashcardsList(data.id);
                }
            } else {
                console.error('Failed to process action:', action);
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            hideLoading(); // Esconde o GIF de carregamento
        }
    };


    const updateMedia = (currentCard) => {
        console.log("Atualizando mídias para o flashcard:", currentCard);

        const questionMediaContainer = document.getElementById('question-media');
        const answerMediaContainer = document.getElementById('answer-media');

        // Atualizar question_media
        if (currentCard.question_media_url) {

            if (
                currentCard.question_media_url.endsWith('.mp4') ||
                currentCard.question_media_url.endsWith('.webm')
            ) {
                questionMediaContainer.innerHTML = `
                <a href="${currentCard.question_media_url}" target="_blank">
                <video controls>
                <source src="${currentCard.question_media_url}" type="video/mp4">
                Your browser does not support the video tag.
                </video>
                </a>`;
            } else if (
                currentCard.question_media_url.endsWith('.gif') ||
                currentCard.question_media_url.endsWith('.jpg') ||
                currentCard.question_media_url.endsWith('.png')
            ) {
                questionMediaContainer.innerHTML = `
                <a href="${currentCard.question_media_url}" target="_blank">
                <img src="${currentCard.question_media_url}" alt="Question media">
                </a>`;
            } else {
                questionMediaContainer.innerHTML = `<p>Unsupported file type.</p>`;
                console.warn("Tipo de arquivo não suportado para question_media_url.");
            }
            questionMediaContainer.style.display = 'block';
        } else {
            questionMediaContainer.style.display = 'none'; // Oculta a div se não houver mídia
        }

        // Atualizar answer_media
        if (currentCard.answer_media_url) {

            if (
                currentCard.answer_media_url.endsWith('.mp4') ||
                currentCard.answer_media_url.endsWith('.webm')
            ) {
                answerMediaContainer.innerHTML = `
                <a href="${currentCard.answer_media_url}" target="_blank">
                <video controls>
                <source src="${currentCard.answer_media_url}" type="video/mp4">
                Your browser does not support the video tag.
                </video>
                </a>`;
            } else if (
                currentCard.answer_media_url.endsWith('.gif') ||
                currentCard.answer_media_url.endsWith('.jpg') ||
                currentCard.answer_media_url.endsWith('.png')
            ) {
                answerMediaContainer.innerHTML = `
                <a href="${currentCard.answer_media_url}" target="_blank">
                <img src="${currentCard.answer_media_url}" alt="Answer media">
                </a>`;
            } else {
                answerMediaContainer.innerHTML = `<p>Unsupported file type.</p>`;
                console.warn("Tipo de arquivo não suportado para answer_media_url.");
            }
            answerMediaContainer.style.display = 'block';
        } else {
            answerMediaContainer.style.display = 'none'; // Oculta a div se não houver mídia
        }

    };



const toggleFlashcard = (flipped) => {
    // Verifica se as mídias existem antes de alterar o display
    const hasQuestionMedia = questionMedia && questionMedia.innerHTML.trim() !== '';
    const hasAnswerMedia = answerMedia && answerMedia.innerHTML.trim() !== '';

    if (flipped) {
        // Mostrar resposta e mídia de resposta (se houver)
        questionCardElement.style.display = 'none';
        answerCardElement.style.display = 'block';

        questionMedia.style.display = 'none'; // Ocultar mídia de pergunta
        answerMedia.style.display = hasAnswerMedia ? 'block' : 'none';
    } else {
        // Mostrar pergunta e mídia de pergunta (se houver)
        questionCardElement.style.display = 'block';
        answerCardElement.style.display = 'none';

        questionMedia.style.display = hasQuestionMedia ? 'block' : 'none';
        answerMedia.style.display = 'none'; // Ocultar mídia de resposta
    }
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

















    // Atualizar flashcard no painel principal
    const updateFlashcard = (flashcard) => {
        questionElement.textContent = flashcard.question;
        answerElement.textContent = flashcard.answer;

        // Reseta para mostrar a pergunta
        questionCardElement.style.display = 'block';
        answerCardElement.style.display = 'none';

        console.log('Flashcard updated:', flashcard);
    };








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
    const flashcardItems = document.querySelectorAll('#flashcards-list li');

    if (!flashcardItems.length) {
        console.error('Nenhum item encontrado na lista de flashcards.');
        return;
    }

    flashcardItems.forEach((item) => {
        // Busca o data-id no elemento <a> dentro do <li>
        const linkElement = item.querySelector('a');
        if (!linkElement) {
            console.warn('Elemento <a> não encontrado dentro de um <li>.');
            return;
        }

        const id = linkElement.getAttribute('data-id');

        if (id === String(cardId)) {
            console.log(`Aplicando destaque ao flashcard ID: ${cardId}`);
            item.classList.add('selected');
            item.classList.remove('easy', 'medium', 'hard', 'no-difficulty'); // Remove todas as classes de dificuldade
            item.classList.add(difficulty || 'no-difficulty'); // Adiciona a nova dificuldade
        } else {
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







const initializeFlashcard = async () => {
    try {
        showLoading(); // Exibe o loader

        // Obtém o ID do flashcard selecionado no localStorage
        const selectedFlashcardId = parseInt(localStorage.getItem('selectedFlashcard'), 10);

        if (!selectedFlashcardId) {
            console.warn('Nenhum flashcard selecionado encontrado no localStorage.');
            hideLoading(); // Esconde o loader
            return;
        }

        // Faz a requisição para obter os dados do flashcard selecionado
        const response = await fetch(`/flashcards/select/`, {
            method: 'POST',
            headers: {
                'x-requested-with': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: new URLSearchParams({ card_id: selectedFlashcardId }),
        });

        if (response.ok) {
            const data = await response.json();

            console.log('Dados carregados do flashcard:', data);

            // Atualiza a interface com os dados do flashcard
            updateMedia(data);
            updateFlashcard(data);
            updateSelectedFlashcard(data);
            updateFlashcardsListStyle(data.id, data.difficulty);
            updateDifficultyButtons(data.difficulty);
        } else {
            console.error('Erro ao carregar o flashcard selecionado:', await response.text());
        }
    } catch (error) {
        console.error('Erro ao inicializar o flashcard:', error);
    } finally {
        hideLoading(); // Esconde o loader
    }
};

await initializeFlashcard();








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




