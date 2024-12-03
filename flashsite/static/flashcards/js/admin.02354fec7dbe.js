document.addEventListener('DOMContentLoaded', function () {
    // Selecionar todos os elementos de question_media e answer_media
    const questionMediaRows = document.querySelectorAll('[data-contentpath="question_media"]');
    const answerMediaRows = document.querySelectorAll('[data-contentpath="answer_media"]');

    questionMediaRows.forEach((questionMediaRow, index) => {
        // Criar botão para cada question_media
        const addQuestionMediaBtn = document.createElement('button');
        addQuestionMediaBtn.textContent = `Add Media to Question`;
        addQuestionMediaBtn.type = 'button';
        addQuestionMediaBtn.classList.add('button');

        // Inserir botão antes do campo correspondente
        questionMediaRow.before(addQuestionMediaBtn);

        // Esconder a linha inicialmente, se o campo estiver vazio
        if (!questionMediaRow.querySelector('input')?.value) {
            questionMediaRow.style.display = 'none';
        } else {
            addQuestionMediaBtn.style.display = 'none';
        }

        // Adicionar evento de clique para exibir o campo
        addQuestionMediaBtn.addEventListener('click', () => {
            questionMediaRow.style.display = 'block';
            addQuestionMediaBtn.style.display = 'none';
        });
    });

    answerMediaRows.forEach((answerMediaRow, index) => {
        // Criar botão para cada answer_media
        const addAnswerMediaBtn = document.createElement('button');
        addAnswerMediaBtn.textContent = `Add Media to Answer`;
        addAnswerMediaBtn.type = 'button';
        addAnswerMediaBtn.classList.add('button');

        // Inserir botão antes do campo correspondente
        answerMediaRow.before(addAnswerMediaBtn);

        // Esconder a linha inicialmente, se o campo estiver vazio
        if (!answerMediaRow.querySelector('input')?.value) {
            answerMediaRow.style.display = 'none';
        } else {
            addAnswerMediaBtn.style.display = 'none';
        }

        // Adicionar evento de clique para exibir o campo
        addAnswerMediaBtn.addEventListener('click', () => {
            answerMediaRow.style.display = 'block';
            addAnswerMediaBtn.style.display = 'none';
        });
    });
});
