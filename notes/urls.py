from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from notes.resources.views import NoteViewSet

router = DefaultRouter()
router.register(r"notes", NoteViewSet, "notes")

urlpatterns = [
    re_path(r"^", include((router.urls, "notes"), namespace="notes")),
]
