from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=Post.Status.PUBLISHED))


class Post(models.Model):
    """ Модель поста """

    class Status(models.TextChoices):
        """ Класс для управления статусом постов блога """
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=250, verbose_name='Название поста', help_text='Напишите название')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField(verbose_name='Содержание поста', help_text='Напишите описание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации поста')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT,
                              verbose_name='Статус состояния поста')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name='Автор поста')
    objects = models.Manager()  # Менеджер, применяемы по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']  # Сортировка постов по дате публикации в порядке убывания
        indexes = [models.Index(fields=['-publish'])]  # Индекс
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ конвертирует логический адрес в физический URL-адрес целевых данных """
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug, ])


class Comment(models.Model):
    """ Модель комментариев """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    name = models.CharField(max_length=100, verbose_name='Автор')
    email = models.EmailField(verbose_name='e-mail')
    body = models.TextField(verbose_name='Комментарии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    active = models.BooleanField(default=True, verbose_name='Статус')

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарии {self.name} к {self.post}'
