from wagtail.admin.panels import FieldPanel
from django.utils.html import format_html


class FlashcardAdminSnippet:
    # Painel personalizado com pré-visualização de mídia
    panels = [
        FieldPanel('question'),
        FieldPanel('question_media'),
        FieldPanel('answer'),
        FieldPanel('answer_media'),
        FieldPanel('difficulty'),
    ]

    def get_admin_display(self):
        # Método para renderizar a miniatura no admin panel
        def preview(media):
            if media and media.name.endswith(('.jpg', '.png', '.gif')):
                return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', media.url)
            elif media and media.name.endswith(('.mp4', '.webm')):
                return format_html('<video src="{}" controls style="max-height: 100px; max-width: 100px;"></video>', media.url)
            return "No preview available"

        return format_html(
            '<div><strong>Question:</strong> {}</div>'
            '<div>{}</div>'
            '<div><strong>Answer:</strong> {}</div>'
            '<div>{}</div>',
            self.question,
            preview(self.question_media),
            self.answer,
            preview(self.answer_media),
        )
