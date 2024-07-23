import pytest
from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, make_many_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize(
    'parametrized_client, page_has_form',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_comment_form_availability(
        parametrized_client,
        page_has_form,
        news_id):
    url = reverse('news:detail', args=(news_id))
    response = parametrized_client.get(url)
    assert ('form' in response.context and isinstance(
        response.context['form'], CommentForm)) is page_has_form


def test_news_order(client, make_many_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news_id, make_many_comments):
    url = reverse('news:detail', args=(news_id))
    response = client.get(url)
    news = response.context['news']
    comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps