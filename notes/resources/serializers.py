from typing import Any, Dict, Hashable, List
from rest_framework import serializers

from notes.models import Note
from notes.models import Tag


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model: Note = Note
        fields: List = [
            "id",
            "title",
            "is_public",
            "body",
            "created_date",
            "modified_date",
        ]

    def create(self, validated_data) -> Note:
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data: Dict[Hashable, Any]) -> Note:
        updated = super().update(instance, validated_data)

        return updated


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Tag = Tag
        fields: List = ["id", "name"]

    def create(self, validated_data) -> Tag:
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data: Dict[Hashable, Any]) -> Tag:
        updated = super().update(instance, validated_data)

        return updated
