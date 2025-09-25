from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Like, Save,Follow
from users.models import CustomUser
import json

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
        self.profile_user = get_object_or_404(CustomUser, username=username)
        return Post.objects.filter(author=self.profile_user).order_by("-created_at")

    User = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user
        context["is_owner"] = (
                self.request.user.is_authenticated and
                self.request.user == self.profile_user
        )
        if self.request.user.is_authenticated and not context["is_owner"]:
            context["is_following"] = Follow.objects.filter(
                follower=self.request.user,
                following=self.profile_user
            ).exists()
        else:
            context["is_following"] = False
        context["post_count"] = Post.objects.filter(author=self.profile_user).count()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            context["total_users"] = User.objects.count()

        return context





@login_required
def save_toggle(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required."}, status=401)

    post = get_object_or_404(Post, id=post_id)
    save, created = Save.objects.get_or_create(user=request.user, post=post)

    if not created:
        save.delete()
        is_saved = False
    else:
        is_saved = True

    return JsonResponse({
        "success": True,
        "is_saved": is_saved,
        "total_saves": post.saves.count()
    })


class Saved(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "login.html")
        saved_posts = Post.objects.filter(saves__user=request.user).order_by("-created_at")
        return render(request, "saved/Saved.html", {
            "posts": saved_posts
        })

class Search(ListView):
    template_name = "search/Search.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(
            list(
                Post.objects.values("id", "text", "created_at", "views", "author__username")
            ),
            default=str,
        )
        return context


class SearchAjax(View):
    def get(self, request):
        q = (request.GET.get('q') or "").strip()
        if not q:
            return JsonResponse({"posts": [], "users": []})
        vector = (
            SearchVector('text', weight='A', config='english')
            + SearchVector('author__username', weight='B', config='english')
        )
        query = SearchQuery(q, config='english')
        posts_qs = (
            Post.objects
            .select_related('author')
            .annotate(search=vector)
            .filter(search=query)
            .annotate(rank=SearchRank(vector, query))
            .order_by('-rank')[:50]
        )

        posts = []
        for p in posts_qs:
            posts.append({
                "id": p.id,
                "text": p.text,
                "author": p.author.username if p.author else None,
                "image": request.build_absolute_uri(p.image.url) if getattr(p, 'image', None) and getattr(p.image, 'url', None) else None,
                "video": request.build_absolute_uri(p.video.url) if getattr(p, 'video', None) and getattr(p.video, 'url', None) else None,
                "rank": getattr(p, 'rank', 0),
            })
        User = get_user_model()
        users_qs = User.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )[:20]
        users = []
        auth_user = request.user if request.user.is_authenticated else None
        for u in users_qs:
            try:
                followers_count = Follow.objects.filter(following=u).count()
            except Exception:
                followers_count = 0
            is_following = False
            if auth_user:
                is_following = Follow.objects.filter(follower=auth_user, following=u).exists()
            users.append({
                "username": u.username,
                "full_name": f"{u.first_name or ''} {u.last_name or ''}".strip(),
                "avatar": request.build_absolute_uri(u.profile_picture.url) if getattr(u, 'profile_picture', None) and getattr(u.profile_picture, 'url', None) else None,
                "profile_url": request.build_absolute_uri(f"/profile/@{u.username}/"),
                "followers_count": followers_count,
                "is_following": is_following,
                "is_self": (auth_user == u),
                "id": u.id,
            })

        return JsonResponse({"posts": posts, "users": users})

class VideoPostUpload(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["text", "video"]
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

@require_POST
@login_required
def like_toggle(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required."}, status=401)

    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return JsonResponse({
        "success": True,
        "is_liked": is_liked,
        "total_likes": post.like_users.count()
    })



User = get_user_model()

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return JsonResponse({"success": False, "error": "O‘zingizni follow qila olmaysiz."}, status=400)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True

    return JsonResponse({
        "success": True,
        "is_following": is_following,
        "followers_count": target_user.followers.count()
    })



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('app:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form, 'post': post})
