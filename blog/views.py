from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from blog.forms import EmailPostForm
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
                             publish__month=month, publish__day=day,)
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    """ Извлекает пост по индентификатору id """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})
