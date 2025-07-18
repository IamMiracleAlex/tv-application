from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Subscribe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def index(request, tag_slug=None):
    object_list = Post.objects.filter(status='publish')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an intger deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #  if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts,
                                                'page': page, 'tag': tag})


def detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create from object but don't save to the db
            new_comment = comment_form.save(commit=False)
            new_comment.post = post # assign current post to the comment
            new_comment.save() # save comment to db
        
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)

    similar_posts = Post.objects.filter(status='publish').filter(
                                        tags__in=post_tags_ids).exclude(id=post.id)

    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
                                        '-same_tags','-publish')[:4]
        
    return render(request, 'blog/detail.html', {'post':post, 'comments': comments,
                                                'new_comment': new_comment, 'comment_form': comment_form,
                                                'similar_posts': similar_posts})



def share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'collinsalex50@gmail.com', [cd['to']])

            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,
                                                'form': form,
                                                'sent': sent})


def subscribe(request):
    if request.method == 'POST':
        sub = Subscribe(email=request.POST['email'])
        sub.save()
        messages.success(request, 'Your subscription was successfull!')
        return redirect('blog:index')


# def search(request):
#     results = []
#     query = None
    
#     if 'query' in request.GET:
#         query = request.GET['query']

#         search_vector = SearchVector('title', 'body')
#         search_query = SearchQuery(query)
#         results = Post.objects.annotate(search=search_vector, rank=SearchRank                                         (search_vector, search_query)).filter                                             (search=search_query).order_by('-rank')

#     return render(request, 'blog/search.html', {'search_value': request.GET,
#                                                 'query': query, 'results': results})


def search(request):
    results = []
    query = None
    
    if 'query' in request.GET:
        query = request.GET['query']

        results = Post.objects.filter(title__icontains=query)
    return render(request, 'blog/search.html', {'query': query,
                                            'results': results})


def about(request):
    return render(request, 'blog/about.html', {})