  
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,

    CommentCreateView,
    CommentDetailView,
    CommentUpdateView,
    CommentDeleteView,


    subscribe_post,
    unsubscribe_post,
    user_notifications_get
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/notifications', user_notifications_get, name='user-notifications'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_id>/comments/new', CommentCreateView.as_view(), name='post-comment-create'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('post/<int:post_id>/subscribe', subscribe_post, name='post-subscription'),
    path('post/<int:post_id>/unsubscribe', unsubscribe_post, name='post-unsubscription'),

    path('about/', views.about, name='blog-about'),
]