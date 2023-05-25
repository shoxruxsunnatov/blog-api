from django.urls import path

from posts.views import (
    CategoriesView,
    CategoryDetailView,
    PostView,
    PostDetailView,
    ReactionView,
    CommentView,
    CommentDetailView
)

app_name = 'posts'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('', PostView.as_view(), name='posts'),
    path("<slug:slug>/reaction/", ReactionView.as_view(), name="reaction"),
    path('<slug:slug>/comments/', CommentView.as_view(), name='comments'),
    path('<slug:slug>/comments/<int:pk>/', CommentDetailView.as_view(), name='comments_detail'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

]