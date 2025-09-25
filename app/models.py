from django.urls import reverse
from django.db import models
from django.conf import settings
from pydub.utils import mediainfo


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('app:home')

    @property
    def total_likes(self):
        return self.like_users.count()

    @property
    def total_saves(self):
        return self.saves.count()

    def __str__(self):
        return f"Posted by {self.author} at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like_users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='saves', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    voice = models.FileField(upload_to='voices/', blank=True, null=True)  # voice comment
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.voice:
            info = mediainfo(self.voice.path)
            duration = float(info['duration'])
            if duration > 15:
                from django.core.exceptions import ValidationError
                raise ValidationError("Voice comment 15 soniyadan uzun bo'lishi mumkin emas!")

    def __str__(self):
        return f"{self.author.username} - {self.text[:20] if self.text else '🎤 Voice Comment'}"

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} → {self.following}"
