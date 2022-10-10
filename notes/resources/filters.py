from typing import Dict

from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    BooleanFilter,
    ModelChoiceFilter,
)

from notes.models import Note
from notes.models import Tag


class NoteFilterSet(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="iexact")
    is_public = BooleanFilter(field_name="is_public", lookup_expr="iexact")
    user = ModelChoiceFilter(
        field_name="note__user", to_field_name="user", queryset=Note.objects.all()
    )
    # tags = ... TODO

    class Meta:
        model = Note
        fields: Dict = {}


class TagFilterSet(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="iexact")
    is_active = BooleanFilter(field_name="is_active", lookup_expr="iexact")

    class Meta:
        model = Tag
        fields: Dict = {}
