from django.urls import path
from .views import posts_view, posts_detail, PostsAPIView, PostDetailsAPIView, PostsGenericAPIView, PostDetailsGenericAPIView

urlpatterns = [
  # path('posts/', posts_view, name="posts"),
  # path('details/<int:pk>/', posts_detail, name="detail"),

  path('posts/<int:pk>/', PostDetailsGenericAPIView.as_view(), name="detail"),
  path('posts/', PostsGenericAPIView.as_view(), name="posts"),
  # path('details/<int:pk>/', PostDetailsGenericAPIView.as_view(), name="detail"),
]