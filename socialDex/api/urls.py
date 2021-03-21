from django.urls import path
from .views import (
    posts_list_view,
    posts_json_all_view,
    posts_json_24h_view,
    new_post_view,
    detail_post_view,
)

urlpatterns = [
    path('posts/', posts_list_view, name='posts-list-view'),
    path('posts/json', posts_json_all_view, name='posts-json-list-view'),
    path('posts/json/24h', posts_json_24h_view, name='posts-json-24h-view'),
    path('posts/new/', new_post_view, name='posts-new-view'),
    path('posts/<int:id>/', detail_post_view, name='posts-detail-view'),
]