from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .constants import POSTS_ON_MAIN_PAGE
from .models import Post, Category


def get_filtered_posts():
    """Возвращает отфильтрованные посты."""
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def index(request):
    """Главная страница проекта."""
    posts = get_filtered_posts()[:POSTS_ON_MAIN_PAGE]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(
        get_filtered_posts(),
        pk=post_id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_filtered_posts().filter(category=category)
    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category.html', context)
