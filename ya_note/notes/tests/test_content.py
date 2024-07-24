from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNotesListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_user = User.objects.create(username='User1')
        cls.second_user = User.objects.create(username='User2')
        cls.first_note = Note.objects.create(
            title='Note1', text='Text', author=cls.first_user, slug='note1')
        cls.second_note = Note.objects.create(
            title='Note2', text='Text2', author=cls.first_user, slug='note2')
        cls.third_note = Note.objects.create(
            title='Note3', text='Text3', author=cls.second_user, slug='note3')
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
        cls.user = User.objects.create(username='User')
        cls.note = Note.objects.create(
            title='Note', text='Text', author=cls.user)
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
