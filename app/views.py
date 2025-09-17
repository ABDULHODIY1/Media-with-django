from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import json

from django.contrib.auth import get_user_model
from .models import Post, Like
from users.models import CustomUser  # agar kerak bo'lsa; yoki get_user_model()

User = get_user_model()

class Home(ListView):
    model = Post
    template_name = "base.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 20


class Blog(ListView):
    template_name = "blog/Blog.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 20


class Chat(TemplateView):
    template_name = "chat/Chat.html"


class ProfileView(ListView):
    model = Post
    template_name = "profile/Profile.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        username = self.kwargs.get("username")
        # agar topilmasa 404 qaytaradi
        self.profile_user = get_object_or_404(CustomUser, username=username)
        return Post.objects.filter(author=self.profile_user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user
        context["is_owner"] = self.request.user.is_authenticated and self.request.user == self.profile_user
        # postlar soni
        context["post_count"] = Post.objects.filter(author=self.profile_user).count()
        return context


class Saved(TemplateView):
    template_name = "saved/Saved.html"


class Search(ListView):
    template_name = "search/Search.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # JSON uchun created_at ni str ga aylantirdim
        context["qs_json"] = json.dumps(
            list(
                Post.objects.values("id", "text", "created_at", "views", "author__username")
            ),
            default=str,
        )
        return context


class SearchAjax(View):
    def get(self, request):
        query = request.GET.get("q", "")
        posts = Post.objects.filter(text__icontains=query).order_by("-created_at")[:20]
        data = [
            {
                "id": post.id,
                "text": post.text,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                "views": post.views if hasattr(post, "views") else 0,
                "author": post.author.username if post.author else None,
                "image": post.image.url if getattr(post, "image", None) else None,
                "video": post.video.url if getattr(post, "video", None) else None,
            }
            for post in posts
        ]
        return JsonResponse(data, safe=False)


# Like toggle: login va POST talab qilinadi
@require_POST
@login_required
def like_toggle(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "message": "Post not found"}, status=404)

    # Like model orqali
    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # allaqachon mavjud bo'lsa, o'chirish
        like_obj.delete()
    total_likes = Like.objects.filter(post=post).count()
    return JsonResponse({"success": True, "total_likes": total_likes})


# Post upload view'lari (mixin'lar CreateView'dan oldin turishi kerak)
class VideoPostUpload(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["text", "video"]  # author avtomatik beriladi
    template_name = "posts/upload.html"
    success_url = reverse_lazy("app:home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoPostUpload(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["text", "image"]
    template_name = "posts/upload.html"
    success_url = reverse_lazy("app:home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
