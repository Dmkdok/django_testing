from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Какая-то новость',
        text='Текст новости'
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        text='Какой-то комментарий',
        author=author,
        news=news
    )


@pytest.fixture
def make_many_news():
    now = timezone.now()
    many_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость номер {index}',
            text='Текст новости',
            date=now - timedelta(days=index)
        )
        many_news.append(news)
    News.objects.bulk_create(many_news)
    return many_news


@pytest.fixture
def make_many_comments(news, author):
    now = timezone.now()
    many_comments = []
    for index in range(12):
        comments = Comment(
            news=news,
            text='Текст комментария',
            author=author,
            created=now - timedelta(days=index)
        )
        many_comments.append(comments)
    Comment.objects.bulk_create(many_comments)
    return many_comments
