from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    """ Отображает общее количество опубликованных постов в блоге """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """ Отображает свежие посты блога на боковой панели """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """ Отображает посты с наибольшим количеством комментариев """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """ Фильтр markdown """
    return mark_safe(markdown.markdown(text))
