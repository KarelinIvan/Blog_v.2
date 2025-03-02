from django.db import models
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    """ Модель поста """

    class Status(models.TextChoices):
        """ Класс для управления статусом постов блога """
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=250, verbose_name='Название поста', help_text='Напишите название')
    slug = models.SlugField(max_length=250)
    body = models.TextField(verbose_name='Содержание поста', help_text='Напишите описание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации поста')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT,
                              verbose_name='Статус состояния поста')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name='Автор поста')

    class Meta:
        # Сортировка постов по дате публикации в порядке убывания
        ordering = ['-publish']
        # Индекс
        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
