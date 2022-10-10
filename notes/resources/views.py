from typing import Any, Dict, Hashable

from rest_framework import viewsets

from notes.resources.serializers import NoteSerializer
from notes.resources.serializers import TagSerializer
from notes.resources.filters import NoteFilterSet
from notes.resources.filters import TagFilterSet
from notes.models import Note
from notes.models import Tag


class NoteViewSet(viewsets.ModelViewSet):
    queryset: Note = Note.objects.all()
    serializer_class: NoteSerializer = NoteSerializer
    filterset_class: NoteFilterSet = NoteFilterSet

    def perform_create(self, serializer: NoteSerializer) -> None:
        serializer.is_valid(raise_exception=True)
        valid_data: Dict[Hashable, Any] = serializer.validated_data
        serializer.save(**valid_data)

    def perform_destroy(self, instance: Note) -> None:
        pass

    def perform_update(self, serializer: NoteSerializer) -> None:
        pass


class TagViewSet(viewsets.ModelViewSet):
    queryset: Tag = Tag.objects.all()
    serializer_class: TagSerializer = TagSerializer
    filterset_class: TagFilterSet = TagFilterSet

    def perform_create(self, serializer: TagSerializer) -> None:
        serializer.is_valid(raise_exception=True)
        valid_data: Dict[Hashable, Any] = serializer.validated_data
        serializer.save(**valid_data)

    def perform_destroy(self, instance: Tag) -> None:
        pass

    def perform_update(self, serializer: TagSerializer) -> None:
        pass
