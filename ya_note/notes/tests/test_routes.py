from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_user = User.objects.create(username='Другой пользователь')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            author=cls.author,
            slug='nazvanie-zametki'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.urls_for_anonymous = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        cls.urls_for_auth = (
            'notes:list',
            'notes:success',
            'notes:add',
        )
        cls.urls_for_note_actions = (
            'notes:detail',
            'notes:edit',
            'notes:delete',
        )

    def test_pages_availability_for_anonymous_user(self):
        for name in self.urls_for_anonymous:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        for name in self.urls_for_auth:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_detail_edit_and_delete(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for name in users_statuses:
                for name in self.urls_for_note_actions:
                    with self.subTest(user=user, name=name):
                        url = reverse(name, args=(self.note.slug,))
                        response = user.get(url)
                        self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = self.urls_for_auth + self.urls_for_note_actions
        for name in urls:
            with self.subTest(name=name):
                args = (self.note.slug,
                        ) if name in self.urls_for_note_actions else None
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
