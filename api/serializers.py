from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Follow, Group, Post, Comment
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    def validate_following(self, value):
        user = self.context['request'].user
        following = value
        is_follow = Follow.objects.filter(user=user, following=following).exists()
        if is_follow:
            raise serializers.ValidationError("Already Subscribed")
        if user == following:
            raise serializers.ValidationError('User can`t subscribe to himself')
        return value

    class Meta:
        fields = '__all__'
        model = Follow
