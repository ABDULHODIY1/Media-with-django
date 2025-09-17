from django.urls import path
from .views import *

app_name = "app"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("blog/", Blog.as_view(), name="blog"),
    path("chat/", Chat.as_view(), name="chat"),
    path("profile/@<str:username>/", ProfileView.as_view(), name="prof"),
    path("saved/", Saved.as_view(), name="saved"),
    path("like-toggle/<int:post_id>/", like_toggle, name="like-toggle"),
    path("search/", Search.as_view(), name="search"),
    path("search/ajax/", SearchAjax.as_view(), name="search-ajax"),
    # URLS For post (trailing slash bilan)
    path("upload/video/", VideoPostUpload.as_view(), name="video_post"),
    path("upload/photo/", PhotoPostUpload.as_view(), name="photo_post"),
]
