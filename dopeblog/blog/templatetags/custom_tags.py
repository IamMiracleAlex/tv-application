from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# filters for adding css classes and html attributes
@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)


# tag for obtaining the total number of blog posts
@register.simple_tag
def total_posts():
    return Post.objects.filter(status='publish').count()


# inclusion tag for showing latest posts
@register.inclusion_tag('partials/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status='publish').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# tag for showing most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.filter(status='publish').annotate(total_comments=Count(
                            'comments')).order_by('-total_comments')[:count] 


                    
# filter to enable markdown functionality
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))