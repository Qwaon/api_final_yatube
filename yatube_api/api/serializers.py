from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Follow, User, Group
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        exclude = ()
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        exclude = ()
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ()
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.CharField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        exclude = ()
        model = Follow

    def validate(self, data):
        following = get_object_or_404(User, username=data['following'])
        user = self.context['request'].user

        if user == following:
            raise serializers.ValidationError(
                {"following": "Вы не можете подписаться на самого себя."},
                code="invalid"
            )

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                {"following": "Вы уже подписаны на этого пользователя."},
                code="unique"
            )

        return data