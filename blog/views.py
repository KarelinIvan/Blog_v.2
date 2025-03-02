from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    """ Выводит список постов """
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """ Выводит детальную информацию о посте, при его отсутствие выдает ошибку код 404 (Не найдено) """
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post_detail.html', {'post': post})
