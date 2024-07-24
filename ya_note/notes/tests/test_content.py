from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNotesListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_user = User.objects.create(username='first_user')
        cls.second_user = User.objects.create(username='second_user')
        cls.first_note = Note.objects.create(
            title='First Note',
            text='Text of the first note',
            author=cls.first_user,
            slug='first-note'
        )
        cls.second_note = Note.objects.create(
            title='Second Note',
            text='Text of the second note',
            author=cls.first_user,
            slug='second-note'
        )
        cls.third_note = Note.objects.create(
            title='Third Note',
            text='Text of the third note',
            author=cls.second_user,
            slug='third-note'
        )
        cls.notes_list_url = reverse('notes:list')

    def test_notes_in_object_list(self):
        self.client.force_login(self.first_user)
        response = self.client.get(self.notes_list_url)
        object_list = response.context['object_list']
        self.assertIn(self.first_note, object_list)
        self.assertIn(self.second_note, object_list)
        self.assertNotIn(self.third_note, object_list)

    def test_other_users_notes_not_in_object_list(self):
        self.client.force_login(self.second_user)
        response = self.client.get(self.notes_list_url)
        object_list = response.context['object_list']
        self.assertIn(self.third_note, object_list)
        self.assertNotIn(self.first_note, object_list)
        self.assertNotIn(self.second_note, object_list)


class TestNoteFormPages(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='test_user')
        cls.test_note = Note.objects.create(
            title='Test Note',
            text='Text for testing',
            author=cls.test_user,
            slug='test-note'
        )
        cls.create_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=[cls.test_note.slug])

    def test_create_note_page_has_form(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.create_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_has_form(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
