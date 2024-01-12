from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Post, Group
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer)
from .permissions import IsAuthorOrReadOnlyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_post(self, **kwargs):
        """Получаем пост с нужным id."""

        post = get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        )
        return post

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
