from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

class TestRoute(TestCase):
    """Тестирование маршрутов."""
    @classmethod
    def setUpTestData(cls):
        # cls.anon = User.objects.create(username='anonymous')
        cls.user = User.objects.create(username='testUser')
        cls.note = Note.objects.create(
            title='Test note',
            text='Test text',
            author=cls.user
        )
        cls.client = Client()
    
    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest():
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_actions_with_notes(self):
        self.client.force_login(self.user)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
        )
        for name, args in urls:
            with self.subTest():
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
        )
        for name, args in urls:
            with self.subTest():
                url = reverse(name, args=args)
                redirect_url = f'''{reverse('users:login')}?next={url}'''
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    # def test_redirect_after_adding_note(self):
    #     self.client.force_login(self.user)
    #     redirect_url = 
    #     response = self.client.get(reverse('notes:success'))
    #     self.assertRedirects(response, redirect_url)
