from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post


class PostListView(ListView):
    """ Класс для вывода списка постов """
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


# def post_list(request):
#     """ Выводит список постов """
#     post_list = Post.published.all()
#     # Постраничная разбивка по 3 поста на страницу
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Если page_number не целое число, то выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если page_number находиться вне диапазона, то выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """ Выводит детальную информацию о посте, при его отсутствие выдает ошибку код 404 (Не найдено) """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day, )
    # Список активных комментариев к посту
    comments = post.comments.filter(active=True)
    # Форма для комментариев пользователя
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    """ Извлекает пост по индентификатору id """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} рекомендует тебе прочитать {post.title}")
            message = (f"Прочитай {post.title} в {post_url}\n"
                       f"{cd['name']} комментариях: {cd['comments']}\n")
            send_mail(subject, message, 'ivan.karelin.1993@mail.ru', [cd['to']])
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent
                  }
                  )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})
