from rest_framework import viewsets 
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instanse.author != self.request.user:
            raise PermissionDenied('Изменять пост может только его автор!')
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удалять пост может только его автор!')
        super().perform_destroy(instance)

    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

