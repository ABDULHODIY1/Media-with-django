from django.db import models
from django.conf import settings
from django.urls import reverse

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

    def _number_typer(self, number):
        """Helper method to convert number to short format like 1.2K, 1M"""
        if number < 1000:
            return str(number)
        elif number < 1_000_000:
            return f"{number / 1000:.1f}K".rstrip('0').rstrip('.')
        else:
            return f"{number / 1_000_000:.1f}M".rstrip('0').rstrip('.')

    def is_media(self):
        return self.image or self.video

    def __str__(self):
        return f"Posted by {self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like_users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.text[:20]}"

