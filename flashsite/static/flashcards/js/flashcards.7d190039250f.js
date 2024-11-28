<script>
    document.addEventListener("DOMContentLoaded", () => {
        const flashcards = document.querySelectorAll(".flashcard");

        flashcards.forEach(flashcard => {
            flashcard.addEventListener("click", () => {
                const flipForm = flashcard.querySelector("#flip-form");
                if (flipForm) {
                    flipForm.submit(); // Submete o formulário oculto
                }
            });
        });
    });
</script>
