from rest_framework import serializers

from posts.models import Category, Post, Reaction, Comment, User


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug'
        )
    


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'category',
            'author'
        )


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'slug',
            'author',
            'likes',
            'dislikes',
            'category',
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategorySerializer(instance.category).data
        return data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ("id", "post", "user", "parent", "text")
        read_only_fields = ("id", "user")


class ReactionSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Reaction.ReactionType.choices)
