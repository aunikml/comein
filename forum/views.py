from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Forum, Post, Reply, ResourceLink
from .forms import PostForm, ReplyForm, ForumForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

@login_required
def forum_list(request):
    forums = Forum.objects.all()
    query = request.GET.get('q')
    if query:
        forums = forums.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(posts__title__icontains=query) |
            Q(posts__content__icontains=query) |
            Q(posts__replies__content__icontains=query)
        )

    context = {
        'forums': forums,
        'query': query
    }
    return render(request, 'forum/forum_list.html', context)

@login_required
def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    posts = forum.posts.all().order_by('-created_at')  # Order posts by creation time
    form = PostForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'post_id' in request.POST:  # Check if it's a reply submission
            post_id = request.POST['post_id']
            post = get_object_or_404(Post, id=post_id)
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.post = post
                reply.created_by = request.user
                reply.save()
                
                # Handle resource links for the reply
                resource_url = request.POST.get('resource_url')
                resource_description = request.POST.get('resource_description')
                if resource_url:
                    ResourceLink.objects.create(reply=reply, url=resource_url, description=resource_description)
                
                return redirect('forum_detail', forum_id=forum.id)
        else: # it is a post submission
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.forum = forum
                post.created_by = request.user
                post.save()

                # Handle resource links for the post
                resource_url = request.POST.get('resource_url')
                resource_description = request.POST.get('resource_description')
                if resource_url:
                    ResourceLink.objects.create(post=post, url=resource_url, description=resource_description)

                return redirect('forum_detail', forum_id=forum.id)

    context = {
        'forum': forum,
        'posts': posts,
        'form': form,
        'reply_form': reply_form,
    }
    return render(request, 'forum/forum_detail.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all().order_by('created_at')  # Order replies chronologically
    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.created_by = request.user
            reply.save()
            return redirect('post_detail', post_id=post.id)

    context = {
        'post': post,
        'replies': replies,
        'reply_form': reply_form,
    }
    return render(request, 'forum/post_detail.html', context)
    
@login_required
def create_forum(request):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to view this page")
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            form.save_m2m()
            return redirect('forum_list')
    else:
        form = ForumForm()
    return render(request, 'forum/create_forum.html', {'form': form})