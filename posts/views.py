from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from posts.serializers import (
    CategorySerializer,
    PostSerializer,
    PostDetailSerializer,
    ReactionSerializer,
    CommentSerializer
)
from posts.models import Category, Post, Reaction, Comment
from paginations import CustomPageNumberPagination
from permissions import IsPostAuthor


class CategoriesView(APIView):
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
    
        return Response(serializer.data)


    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            raise PermissionDenied
        
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CategoryDetailView(CategoriesView):

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        serializer = CategorySerializer(instance=category)

        return Response(serializer.data)


    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    
    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        category.delete()

        return Response(
            {'detail': 'Deleted.'}
        )


class PostDetailView(APIView):
    permission_classes = (IsPostAuthor,)
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        serializer = PostDetailSerializer(instance=post)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PostDetailSerializer)
    def put(self, request, *args, **kwargs):
        
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        
        self.check_object_permissions(request, post)

        serializer = PostDetailSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    
    def delete(self, request, *args, **kwargs):
        
        post = get_object_or_404(Post, slug=kwargs.get('slug'))

        self.check_object_permissions(request, post)

        post.delete()

        return Response(
            {'detail': 'Deleted.'}
        )


class PostView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    queryset = Post.objects.order_by('-id')


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostDetailSerializer
        
        return PostSerializer

    @swagger_auto_schema(request_body=PostDetailSerializer)
    def post(self, request, *args, **kwargs):
        
        request.data.update(
            {
                'author': request.user.id
            }
        )
        serializer = PostDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ReactionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ReactionSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_ = serializer.validated_data.get("type")
        user = request.user
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        reaction = Reaction.objects.filter(post=post, user=user).first()
        if reaction and reaction.type == type_:
            reaction.delete()
        else:
            Reaction.objects.update_or_create(post=post, user=user, defaults={"type": type_})
        data = {"type": type_, "detail": "Liked or disliked."}
        return Response(data)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        data = Comment.objects.filter(post=post)
        serializer = CommentSerializer(data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, *args, **kwargs):
        request.data.update(
            {
                'author': request.user.id
            }
        )
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer)
    def put(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        serializer = CommentSerializer(data=request.data, instance=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, slug=kwargs.get('pk'))
        comment.delete()

        return Response(
            {'detail': 'Deleted.'}
        )