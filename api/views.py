# TODO:  Напишите свой вариант
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions, filters
from .models import Follow, Group, Post, Comment
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner
from rest_framework_simplejwt.authentication import JWTAuthentication


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user)


class APIGroup(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwner,]
    authentication_classes = [JWTAuthentication]


class APIFollow(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user',]
    search_fields = ['user__username','following__username']


    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(following__username=user.username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
