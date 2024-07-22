# notes/tests/test_content.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNotesListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='User1', password='password')
        cls.user2 = User.objects.create(username='User2', password='password')
        cls.note1 = Note.objects.create(title='Note1', text='Text1', author=cls.user1, slug='note1')
        cls.note2 = Note.objects.create(title='Note2', text='Text2', author=cls.user1, slug='note2')
        cls.note3 = Note.objects.create(title='Note3', text='Text3', author=cls.user2, slug='note3')
        cls.url = reverse('notes:list')

    def test_notes_in_object_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)
        self.assertIn(self.note2, object_list)
        self.assertNotIn(self.note3, object_list)

    def test_other_users_notes_not_in_object_list(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        object_list = response.context['object_list']
        self.assertIn(self.note3, object_list)
        self.assertNotIn(self.note1, object_list)
        self.assertNotIn(self.note2, object_list)


class TestNoteFormPages(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='User')
        cls.note = Note.objects.create(title='Note', text='Text', author=cls.user, slug='note')
        cls.create_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=[cls.note.slug])

    def test_create_note_page_has_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_has_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
