from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    """ Выводит список постов """
    post_list = Post.published.all()
    # Постраничная разбивка по 3 поста на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """ Выводит детальную информацию о посте, при его отсутствие выдает ошибку код 404 (Не найдено) """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day,)
    return render(request, 'blog/post/detail.html', {'post': post})
