from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cannot_create_comment(client, form_data, news_id):
    url = reverse('news:detail', args=(news_id))
    comments_before = Comment.objects.count()
    response = client.post(url, data=form_data)
    comments_after = Comment.objects.count()
    login_url = reverse('users:login')
    expected_redirect_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_redirect_url)
    assert comments_before == comments_after


def test_authorized_user_can_create_comment(
        author_client, author, form_data, news_id
):
    url = reverse('news:detail', args=(news_id))
    comments_before = Comment.objects.count()
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_after = Comment.objects.count()
    assert comments_after == comments_before + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_comment_with_bad_words_is_not_created(author_client, news_id):
    bad_words_data = {
        'text': f'Комментарий с запрещенным словом {BAD_WORDS[0]}.'}
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_own_comment(
        author_client, comment, form_data, news_id
):
    url = reverse('news:edit', args=(comment.id,))
    news_url = reverse('news:detail', args=(news_id))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_cannot_edit_other_users_comment(
        not_author_client, comment, form_data
):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_author_can_delete_own_comment(author_client, comment, news_id):
    url = reverse('news:delete', args=(comment.id,))
    news_url = reverse('news:detail', args=(news_id))
    response = author_client.post(url)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 0


def test_author_cannot_delete_other_users_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
