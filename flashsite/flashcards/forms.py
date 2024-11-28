from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.html import strip_tags
from wagtail.admin.forms import WagtailAdminPageForm


class NoTitleForm(WagtailAdminPageForm):
    class Meta:
        model = None  # Este será definido pelo Wagtail no momento do uso
        widgets = {
            'title': forms.HiddenInput(),  # Oculta o campo title
            'slug': forms.HiddenInput(),   # Oculta o campo slug
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa title e slug com valores padrão, se vazios
        if not self.initial.get('title'):
            self.initial['title'] = _('auto-generated-title')
        if not self.initial.get('slug'):
            self.initial['slug'] = _('auto-generated-slug')

    def save(self, commit=True):
        page = super().save(commit=False)

        # Gere o título e o slug com base no campo 'question'
        new_title = strip_tags(self.cleaned_data['question'])
        page.title = new_title
        page.slug = slugify(new_title)

        if commit:
            page.save()
        return page


class FlashcardInteractionForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('next', 'Next'),
            ('previous', 'Previous'),
            ('flip', 'Flip'),
            ('select', 'Select'),
        ],
        required=True,
        widget=forms.HiddenInput(),  # Oculta o campo no frontend
    )
    difficulty = forms.ChoiceField(
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        required=False,
        widget=forms.HiddenInput(),  # Oculta o campo no frontend
    )
    card_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),  # Oculta o campo no frontend
    )