from django.db.models import Count, Prefetch
from django.shortcuts import render
from blog.models import Comment, Post, Tag


def serialized_comments(comment):
    return {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        }


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.first().title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts__count,
    }


def index(request):
    posts = Post.objects.all().prefetch_related(
        Prefetch('author'),
        Prefetch('tags', queryset=Tag.objects.popular()))

    most_popular_posts = posts.popular()[:5].fetch_with_comments_count()
    most_fresh_posts = posts.fresh_posts()[:5].fetch_with_comments_count()
    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    posts = Post.objects.popular().prefetch_related(
        Prefetch('author'),
        Prefetch('tags', queryset=Tag.objects.popular()))

    post = posts.get(slug=slug)
    comments = Comment.objects.prefetch_related('author').filter(post=post)
    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': [serialized_comments(comment) for comment in comments],
        'likes_amount': post.likes.count(),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = posts[:5].fetch_with_comments_count()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    posts = Post.objects.all().prefetch_related(
        Prefetch('author'),
        Prefetch('tags', queryset=Tag.objects.popular()))

    tag = Tag.objects.get(title=tag_title)

    most_popular_tags = Tag.objects.popular()

    most_popular_posts = posts.popular()[:5].fetch_with_comments_count()

    related_posts = tag.posts.all().prefetch_related(
        Prefetch('author'),
        Prefetch('tags', queryset=Tag.objects.popular())).fetch_with_comments_count()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
