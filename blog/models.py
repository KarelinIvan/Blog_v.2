from django.db import models
from django.utils import timezone

class Post(models.Model):
    """ Модель поста """
    title = models.CharField(max_length=250, verbose_name='Название поста', help_text='Напишите название')
    slug = models.SlugField(max_length=250)
    body = models.TextField(verbose_name='Содержание поста', help_text='Напишите описание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации поста')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
