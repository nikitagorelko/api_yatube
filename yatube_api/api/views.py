from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer: ModelSerializer) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet:
        return self.get_post().comments.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
