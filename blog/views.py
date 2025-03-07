from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    """ Выводит список постов """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """ Выводит детальную информацию о посте, при его отсутствие выдает ошибку код 404 (Не найдено) """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
