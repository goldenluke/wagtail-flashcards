document.addEventListener('DOMContentLoaded', function () {
    const questionMediaRow = document.querySelector('[data-contentpath="question_media"]');
    const answerMediaRow = document.querySelector('[data-contentpath="answer_media"]');

    const addQuestionMediaBtn = document.createElement('button');
    addQuestionMediaBtn.textContent = 'Add Media to Question';
    addQuestionMediaBtn.type = 'button';
    addQuestionMediaBtn.classList.add('button');

    const addAnswerMediaBtn = document.createElement('button');
    addAnswerMediaBtn.textContent = 'Add Media to Answer';
    addAnswerMediaBtn.type = 'button';
    addAnswerMediaBtn.classList.add('button');

    // Insert buttons above the respective fields
    questionMediaRow.before(addQuestionMediaBtn);
    answerMediaRow.before(addAnswerMediaBtn);

    // Initially hide media rows
    if (!questionMediaRow.querySelector('input').value) {
        questionMediaRow.style.display = 'none';
    } else {
        addQuestionMediaBtn.style.display = 'none';
    }

    if (!answerMediaRow.querySelector('input').value) {
        answerMediaRow.style.display = 'none';
    } else {
        addAnswerMediaBtn.style.display = 'none';
    }

    // Add event listeners to show the rows
    addQuestionMediaBtn.addEventListener('click', () => {
        questionMediaRow.style.display = 'block';
        addQuestionMediaBtn.style.display = 'none';
    });

    addAnswerMediaBtn.addEventListener('click', () => {
        answerMediaRow.style.display = 'block';
        addAnswerMediaBtn.style.display = 'none';
    });
});
