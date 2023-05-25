import json

from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, Category, Comment, Reaction
from users.models import User

client = Client()


# Category
class TestCategory(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='dasturlash kat', )

    def test_list(self):
        url = reverse('categories')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


class TestBlog(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='dasturlash', )
        self.user = User.objects.create(
            username='admin',
            password='1'
        )

        self.post = Post.objects.create(

            title='backend',
            text='kgegslgjlkdsjglksjglk',
            category=self.category,
            tag=self.tag,
            author=self.user
        )
        client.login(username=self.user.username, password='1')
        self.comment = Comment.objects.create(post=self.post, author=self.user)
        self.like_dislike = Reaction.objects.create(user=self.user, post=self.post)
        self.post_data = {
            "title": 'title1',
            "body": 'body',
            "author": self.user,
            "category": self.category
        }

        self.new_post = {
            "title": "asdasdaasd",
            "text": "wwww",
            "category": self.category.id
        }

        self.comment_data = {
            "content": "asdasdasadasasda"
        }

    def test_post_delete(self):
        url = reverse('post_detail', kwargs={"slug": self.post.slug})
        client.force_login(user=self.user)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_post_get(self):
        url = reverse('post_detail', kwargs={"slug": self.post.slug})
        client.force_login(user=self.user)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        client.force_login(user=self.user)
        url = reverse('posts')
        response = client.post(url, data=self.new_post)

        self.assertEquals(response.status_code, 201)
        self.assertNotEqual(response.status_code, 400)
        self.assertEqual(response.data["title"], self.new_post["title"])



    def test_comment_post(self):
        client.force_login(user=self.user)
        url = reverse('comments', kwargs={"slug": self.post.slug})

        response = client.post(url, data=self.comment_data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 400)

    def test_comment_delete(self):
        client.force_login(user=self.user)
        url = reverse('comments_detail', kwargs={"pk": self.comment.id})
        response = client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_comment_get(self):
        client.force_login(user=self.user)
        url = reverse('comments_detail', kwargs={"pk": self.comment.id})
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_comment_put(self):
        client.force_login(user=self.user)
        url = reverse('comments_detail', kwargs={"pk": self.comment.id})
        data = {
            "content": "65as11a321a3sd",
            "parent": self.comment.id
        }
        response = client.put(url, data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["content"], data["content"])



