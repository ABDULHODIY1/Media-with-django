from django.urls import path
from .views import (
    Home, Blog, Chat, ProfileView, follow_toggle,
    like_toggle, save_toggle, Saved, Search, SearchAjax,
    VideoPostUpload, PhotoPostUpload
)

app_name = 'app'

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("blog/", Blog.as_view(), name="blog"),
    path("chat/", Chat.as_view(), name="chat"),
    path("profile/@<str:username>/", ProfileView.as_view(), name="prof"),
    path('follow-toggle/<str:username>/', follow_toggle, name='follow-toggle'),
    path("like-toggle/<int:post_id>/", like_toggle, name="like_toggle"),
    path("save-toggle/<int:post_id>/", save_toggle, name="save_toggle"),
    path("saved/", Saved.as_view(), name="saved"),
    path("search/", Search.as_view(), name="search"),
    path("search/ajax/", SearchAjax.as_view(), name="search_ajax"),
    path("upload/video/", VideoPostUpload.as_view(), name="video_post"),
    path("upload/photo/", PhotoPostUpload.as_view(), name="photo_post"),
]
