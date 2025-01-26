from django.shortcuts import render , get_object_or_404, redirect, HttpResponse
from .models import Post, NewPost
from django.core.paginator import Paginator
from .form import NewPostForm
from django.utils import timezone
from django.http import HttpResponseForbidden


def index(request):
    return render(request, 'blog/index.html')


def post_list(request):
    posts = NewPost.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_list = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'posts': posts_list})


def post_detail(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})



def about(request):
    return render(request, 'blog/about.html')


def get_contacts(request):
    return render(request, 'blog/contacts.html')


def post_new(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            if NewPost.objects.filter(title=title).exists():
                form.add_error('title', 'Пост с таким заголовком уже существует')
            else:
                post = form.save(commit=False)
                if 'save_as_draft'not in request.POST:
                    post.publiched_date = timezone.now()
                else:
                    post.published_date = None
                post.save()
                return redirect('post_detail', pk=post.pk)
    else:
        form = NewPostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту запись")
    if request.method == "POST":
        form = NewPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = NewPostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    
def post_draft(request):
    posts = NewPost.objects.filter(published_date__insull=True).order_by('created_date')
    return render(request, 'blog/post_draft.html', {'posts': posts})



def post_info(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    return render(request, 'blog/post_info.html', {'post': post})



def post_published(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('Вы не можете опубликовать эту запись')
    post.publish()
    return redirect('post_info', pk=pk)

def post_del(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('Вы не можете удалять эту запись')
    post.delete()
    return redirect('post_draft')