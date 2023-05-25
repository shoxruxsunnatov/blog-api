import random
from django.db import models
from django.utils.text import slugify

from users.models import User


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=300)
    slug  = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        slug = self.slug
        while self.__class__.objects.filter(slug=slug).exists():
            slug = f"{self.slug}-{random.randint(1, 100000)}"
        self.slug = slug
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Post(TimestampModel):
    title = models.CharField(max_length=300)
    text  = models.TextField()
    slug  = models.SlugField(null=True, blank=True)
    date  = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='author', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.title)
            slug = self.slug
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{self.slug}-{random.randint(1, 100000)}"
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:50]


class Comment(TimestampModel):
    text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user', null=True)

    parent = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, related_name='parent_comment', null=True)

    def __str__(self):
        return str(self.user)


class Reaction(TimestampModel):
    class ReactionType(models.IntegerChoices):
        DISLIKE = -1
        LIKE = 1

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_dislike")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_dislike")
    type = models.SmallIntegerField(choices=ReactionType.choices)

    class Meta:
        unique_together = ["post", "user"]

    def __str__(self):
        return f"{self.user}"
    

