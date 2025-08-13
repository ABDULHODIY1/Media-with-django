from django.urls import path
from .views import *

app_name = "app"

urlpatterns = [
    path('',Home.as_view(), name = "home"),
    path('blog',Blog.as_view(), name = "blog"),
    path('chat', Chat.as_view(), name="chat"),
    path('profile/@<str:username>/', ProfileView.as_view(), name='prof'),
    path('saved', Saved.as_view(), name="saved"),
    path('search', Search.as_view(), name="search"),
    path('like-toggle/<int:post_id>/', like_toggle, name='like-toggle'),

    # URLS For post
    path("upload_vp",VideoPostUpload.as_view(),name = "video_post")
    

]

