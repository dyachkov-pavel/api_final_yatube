from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Follow, Group, Post, Comment
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, 
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')

    def validate_following(self, value):
        user = self.context['request'].user
        following = value
        if user == following:
            raise serializers.ValidationError('User can`t subscribe to himself')
        return value

    class Meta:
        fields = '__all__'
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
