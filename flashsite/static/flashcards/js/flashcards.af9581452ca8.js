    document.addEventListener("DOMContentLoaded", () => {
        const flashcards = document.querySelectorAll(".flashcard");

        flashcards.forEach(flashcard => {
            flashcard.addEventListener("click", () => {
                const form = flashcard.querySelector(".hidden-flip-form");
                if (form) {
                    form.submit(); // Submete o formulário oculto
                }
            });
        });
    });
