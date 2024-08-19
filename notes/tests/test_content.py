from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from notes.models import Note


class TestHomePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        for index in range(10):
            note = Note.objects.create(
                news=cls.news, author=cls.author, text=f'Tекст {index}',
            )
            # note.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
            note.save()