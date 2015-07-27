from django import template
from micro_blog.models import Tags, Category, Post
from pages.models import Menu
from django.db.models import Count

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_tags(context):
    return Tags.objects.annotate(Num=Count('rel_posts')).filter(Num__gt = 0)[:20]


@register.assignment_tag(takes_context=True)
def get_categories(context):
    has_blog_posts_categories = []
    categories = Category.objects.filter(is_display=True)
    for category in categories:
        if Post.objects.filter(category_id=category.id).exists():
            has_blog_posts_categories.append(category)
    return has_blog_posts_categories


@register.assignment_tag(takes_context=True)
def get_latest_posts(context):
    return Post.objects.filter(status='P').order_by('-created_on')[:10]


@register.assignment_tag(takes_context=True)
def get_menus(context):
    return Menu.objects.filter(parent = None, status="on").order_by('lvl')
