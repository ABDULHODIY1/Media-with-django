from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import Post
from users.models import CustomUser  # yoki Profile
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post, Like
User = get_user_model()  # ✅ bu to‘g‘ri

# Create your views here.

class Home(ListView):
    model = Post
    template_name = ("base.html")
    context_object_name = "posts"
    ordering = ['-created_at']  # yangi postlar birinchi bo‘ladi
    ...

@csrf_exempt
def like_toggle(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            post = Post.objects.get(pk=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                like.delete()
            total_likes = post.like_users.count()
            return JsonResponse({'success': True, 'total_likes': total_likes})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Post not found'})
    return JsonResponse({'success': False, 'message': 'Unauthorized'})


class Blog(ListView):
    template_name = "blog/Blog.html"
    model = Post
    context_object_name = "posts"
    ordering = ['-created_at']  # yangi postlar birinchi bo‘ladi
    ...

class Chat(TemplateView):
    template_name = "chat/Chat.html"
    ...



class ProfileView(ListView):
    model = Post
    template_name = 'profile/Profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.profile_user = CustomUser.objects.get(username=username)
        return Post.objects.filter(author=self.profile_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user  # <- kerak!
        context['is_owner'] = self.request.user == self.profile_user
        return context
    ...

class Saved(TemplateView):
    template_name = "saved/Saved.html"
    ...

class Search(ListView):
    template_name = "search/Search.html"
    model = Post
    context_object_name = "posts"
    ordering = ['-created_at']  # yangi postlar birinchi bo‘ladi
    ...

class VideoPostUpload(CreateView,LoginRequiredMixin):
    model = Post
    fields = [
        "text",
        "video",
        "author",
    ]
    template_name = "posts/upload.html"

    def querySearchMentation(self, users):...

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)