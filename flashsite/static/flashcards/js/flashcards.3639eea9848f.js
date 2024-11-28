    document.addEventListener("DOMContentLoaded", () => {
        // Seleciona o flashcard container e o formulário oculto
        const flashcardContainer = document.getElementById("flashcard-container");
        const flipForm = document.getElementById("flip-form");

        if (flashcardContainer && flipForm) {
            // Adiciona o evento de clique ao container do flashcard
            flashcardContainer.addEventListener("click", () => {
                flipForm.submit(); // Submete o formulário oculto
            });
        } else {
            console.error("Flashcard container ou formulário flip não encontrados.");
        }
    });
