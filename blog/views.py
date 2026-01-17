from django.shortcuts import render, get_object_or_404

from django.utils import timezone

from .models import Post, Category


def index(request):
    """Главная страница проекта."""
    posts = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )[:5]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(
        Post.objects.select_related(
            'author', 'location', 'category'
        ),
        pk=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
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
    posts = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category.html', context)
