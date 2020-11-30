from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from .forms import *
from django.contrib import messages
from Accounts.forms import UserRegisterForm, UserUpdateForm
from Accounts.views import login_excluded
from django.contrib.auth.decorators import login_required
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request,'post_list.html',context)


def post_detail(request,id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post,reply=None).order_by('id')
    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()

    comment_form = CommentCreateForm()
    context = {
        'post':post,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'post_detail.html',context)

@login_required
def post_create(request):
    if request.method == 'POST':
         form = PostCreateForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect('post_list')
    else:
        form = PostCreateForm()
    context = {
        'form':form,
    }
    return render(request,'post_create.html',context) 

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    messages.warning(request, 'post has been successfully deleted!')
    return redirect('post_list')

@login_excluded('post_list')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        a_form = UserUpdateForm(request.POST, instance=request.user)
        if a_form.is_valid():
            a_form.save()
            return redirect('profile')
    else:
        a_form = UserUpdateForm(instance=request.user)
        context = {'a_form': a_form}
    return render(request, 'profile.html', context)

def support(request):
    return render(request, 'support.html', {'title': 'Support'})

def about(request):
    return render(request, 'about.html', {'title': 'About'})