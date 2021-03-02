from django.test import TestCase
from Posts.models import Post, Comment
from django.contrib.auth.models import User

class TestPostModel(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='my_nickname',
            email='name@invalid.com',
        )
        self.user1.set_password("my_paSW1")
        self.user1.save()

        self.user2 = User.objects.create(
            username='my_nickname2',
            email='name2@invalid.com',
        )
        self.user2.set_password("my_paSW2")
        self.user2.save()

        self.post1 = Post.objects.create(
            user=self.user1,
            post_text='This is my first post',
        )
        self.post2 = Post.objects.create(
            user=self.user1,
            post_text='Second-post',
        )

    def test_slug(self):
        self.assertEquals(self.post1.slug, 'this-is-my-first-pos')
        self.assertEquals(self.post2.slug, 'second-post')

    def test_total_likes_count(self):
        self.assertEquals(self.post1.total_likes, 0)
        self.post1.users_like.add(self.user1)
        self.post1.total_likes_count()
        self.assertEquals(self.post1.total_likes, 1)

        self.post1.users_like.add(self.user2)
        self.post1.total_likes_count()
        self.assertEquals(self.post1.total_likes, 2)
