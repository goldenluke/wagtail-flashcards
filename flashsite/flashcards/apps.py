from django.apps import AppConfig


class FlashcardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flashcards'

    def ready(self):
        import flashcards.admin  # Importa manualmente o admin

class FlashcardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flashcards'

    def ready(self):
        import flashcards.signals  # Importa os sinais
