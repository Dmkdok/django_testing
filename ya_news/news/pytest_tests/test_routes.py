from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url_name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_pages_accessible_for_anonymous_user(client, url_name, args):
    url = reverse(url_name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'url_name',
    (
        'news:edit',
        'news:delete',
    )
)
def test_availability_edit_delete_comment_for_different_users(
        parametrized_client, url_name, comment, expected_status
):
    url = reverse(url_name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name',
    (
        'news:edit',
        'news:delete',
    )
)
def test_anonymous_user_redirects_to_login(client, url_name, comment):
    login_url = reverse('users:login')
    url = reverse(url_name, args=(comment.id,))
    expected_redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_redirect_url)
