from django.shortcuts import render
from .models import Post
from .forms import PostForm
import markdown2

def upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            post_html = markdown2.markdown(file.read())
            post = Post(title=title, body=post_html)
            post.save()
            return render(request, 'resources/upload.html', {'form': form, 'success': True})

    return render(request, 'resources/upload.html')

def postlist(request):
    posts = Post.objects.all()
    return render(request, 'resources/postlist.html', {'posts': posts})

def post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'resources/post.html', {'post': post})