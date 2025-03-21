from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from blog.forms import EmailPostForm, CommentForm, SearchForm
from blog.models import Post
from taggit.models import Tag
from django.db.models import Count


# class PostListView(ListView):
#     """ Класс для вывода списка постов """
#     queryset = Post.objects.all()
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """ Выводит список постов """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Постраничная разбивка по 3 поста на страницу
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находиться вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    """ Выводит детальную информацию о посте, при его отсутствие выдает ошибку код 404 (Не найдено) """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day, )
    # Список активных комментариев к посту
    comments = post.comments.filter(active=True)
    # Форма для комментариев пользователя
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


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
    """ Функция для записи комментариев к постам """
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


def post_search(request):
    """ Функция для поиска опубликованных постов """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query), ).filter(
                    search=search_query).order_by('-rank'))

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
