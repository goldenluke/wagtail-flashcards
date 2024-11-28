from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from flashcards.views import flashcard_view

from search import views as search_views

from flashcards.views import copy_flashcards_index, import_flashcards, flashcard_interaction, flashcards_list, select_flashcard, assign_difficulty

from django.conf.urls.static import static

urlpatterns = [
    path('flashcards/', flashcard_view, name='flashcards'),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('clone-flashcards/<int:page_id>/', copy_flashcards_index, name='copy_flashcards_index'),  # Para clonar flashcards
    path('<str:username>/<int:page_id>/', flashcard_view, name='flashcard_view'),
    path('import-flashcards/<int:page_id>/', import_flashcards, name='import_flashcards'),
    path('accounts/', include('allauth.urls')),  # Add Allauth URLs
    path('flashcards/interaction/', flashcard_interaction, name='flashcard_interaction'),
    path('flashcards/list/', flashcards_list, name='flashcards_list'),
    path('flashcards/select/', select_flashcard, name='select_flashcard'),
    path('flashcards/difficulty/', assign_difficulty, name='assign_difficulty'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
