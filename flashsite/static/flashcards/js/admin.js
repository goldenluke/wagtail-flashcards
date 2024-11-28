document.addEventListener('DOMContentLoaded', () => {
    const questionMediaField = document.querySelector('#id_question_media');
    const answerMediaField = document.querySelector('#id_answer_media');

    // Esconde os campos inicialmente
    questionMediaField.closest('.object').style.display = 'none';
    answerMediaField.closest('.object').style.display = 'none';

    // Adiciona botões para exibir os campos
    const questionMediaButton = document.createElement('button');
    questionMediaButton.type = 'button';
    questionMediaButton.textContent = 'Add Question Media';
    questionMediaButton.classList.add('button');
    questionMediaField.closest('.field').prepend(questionMediaButton);

    questionMediaButton.addEventListener('click', () => {
        questionMediaField.closest('.object').style.display = '';
    });

    const answerMediaButton = document.createElement('button');
    answerMediaButton.type = 'button';
    answerMediaButton.textContent = 'Add Answer Media';
    answerMediaButton.classList.add('button');
    answerMediaField.closest('.field').prepend(answerMediaButton);

    answerMediaButton.addEventListener('click', () => {
        answerMediaField.closest('.object').style.display = '';
    });
});
