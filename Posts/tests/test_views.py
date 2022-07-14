from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from Accounts.models import Profile
from Posts.models import Post, Comment
from Posts.views import like_post
from django.contrib.auth.models import User


User = get_user_model()

class TestPostViews(TestCase):

    def setUp(self):
        # 1st user
        self.user1 = User.objects.create(
            username='my_nickname',
            email='name@invalid.com',
        )
        self.user1.set_password("my_paSW1")
        self.user1.save()

        self.profile1 = Profile.objects.create(
            user=self.user1
        )

        # 2nd user
        self.user2 = User.objects.create(
            username='my_nickname2',
            email='name2@invalid.com',
        )
        self.user2.set_password("my_paSW2")
        self.user2.save()

        self.profile2 = Profile.objects.create(
            user=self.user2
        )

        # 1st post
        self.post1 = Post.objects.create(
            user=self.user1,
            post_text="Initial post",
            slug='initial-post'
        )

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_post_exists(self):
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 1)

    def test_add_valid_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')

        url = reverse('Posts:add_post')
        response = self.client.post(
            url, {
                'post_text': 'This is some post text',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.all().count(), 2)

    def test_add_invalid_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')

        url = reverse('Posts:add_post')
        response = self.client.post(
            url, {
                'post_text': '',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.all().count(), 1)

    def test_view_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')

        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:post_view', args=[
            self.user1.username, post_id, 'initial-post'
        ])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Posts/post_details.html')
        self.assertEquals(Post.objects.all().count(), 1)

    def test_edit_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:edit_post', args=[post_id])
        response = self.client.post(
            url, {
                'post_text': 'edited post',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.filter(
            post_text='edited post'
        ).count(), 1)

    def test_edit_post_not_by_author(self):
        self.client.login(username=self.user2.username,
                          password='my_paSW2')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:edit_post', args=[post_id])
        response = self.client.post(
            url, {
                'post_text': 'edited post',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.filter(
            post_text='Initial post'
        ).count(), 1)

    def test_invalid_edit_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:edit_post', args=[post_id])
        response = self.client.post(
            url, {
                'post_text': '',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Posts/edit_post.html')
        self.assertEquals(Post.objects.filter(
            post_text='Initial post'
        ).count(), 1)

    def test_delete_post(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:delete_post', args=[post_id])

        response = self.client.post(url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.all().count(), 0)

    def test_delete_post_not_by_author(self):
        self.client.login(username=self.user2.username,
                          password='my_paSW2')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:delete_post', args=[post_id])

        response = self.client.post(url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Post.objects.all().count(), 1)

    def test_like_and_unlike_post(self):
        self.factory = RequestFactory()
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:like_post', args=[post_id])
        request = self.factory.post(url)
        request.user = self.user1
        response = like_post(request, post_id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=post_id).total_likes, 1)

        response = like_post(request, post_id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=post_id).total_likes, 0)


class TestCommentViews(TestCase):

    def setUp(self):
        # 1st user
        self.user1 = User.objects.create(
            username='my_nickname',
            email='name@invalid.com',
        )
        self.user1.set_password("my_paSW1")
        self.user1.save()

        self.profile1 = Profile.objects.create(
            user=self.user1
        )

        # 2nd user
        self.user2 = User.objects.create(
            username='my_nickname2',
            email='name2@invalid.com',
        )
        self.user2.set_password("my_paSW2")
        self.user2.save()

        self.profile2 = Profile.objects.create(
            user=self.user2
        )

        # 1st post
        self.post1 = Post.objects.create(
            user=self.user1,
            post_text="Initial post",
            slug='initial-post'
        )

        # 2nd post
        self.post2 = Post.objects.create(
            user=self.user2,
            post_text="second post",
            slug='second-post'
        )

        # 1st comment
        self.post1 = Comment.objects.create(
            author=self.user1,
            post=self.post1,
            comment_text="Initial comment",
        )

    def test_post_exists(self):
        user_count = Post.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_posts_exists(self):
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 2)

    def test_comments_exists(self):
        comment_count = Comment.objects.all().count()
        self.assertEqual(comment_count, 1)

    def test_add_valid_comment(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:add_comment', args=[post_id])
        response = self.client.post(
            url, {
                'comment_text': 'This is some comment text',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.all().count(), 2)

    def test_add_invalid_comment(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        post_id = Post.objects.get(slug='initial-post').id
        url = reverse('Posts:add_comment', args=[post_id])
        response = self.client.post(
            url, {
                'comment_text': '',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.all().count(), 1)

    def test_remove_comment(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        comment_id = Comment.objects.get(comment_text="Initial comment").id
        url = reverse('Posts:remove_comment', args=[comment_id])
        response = self.client.post(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.all().count(), 0)

    def test_reject_removing_comment_not_by_author(self):
        self.client.login(username=self.user2.username,
                          password='my_paSW2')
        comment_id = Comment.objects.get(comment_text="Initial comment").id
        url = reverse('Posts:remove_comment', args=[comment_id])
        response = self.client.post(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.all().count(), 1)

    def test_edit_comment(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        comment_id = Comment.objects.get(comment_text="Initial comment").id
        url = reverse('Posts:edit_comment', args=[comment_id])
        response = self.client.post(
            url, {
                'comment_text': 'edited comment',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.filter(
            comment_text='edited comment'
        ).count(), 1)

    def test_invalid_edit_comment(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        comment_id = Comment.objects.get(comment_text="Initial comment").id
        url = reverse('Posts:edit_comment', args=[comment_id])
        response = self.client.post(
            url, {
                'comment_text': '',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Posts/edit_comment.html')
        self.assertEquals(Comment.objects.filter(
            comment_text='Initial comment'
        ).count(), 1)

    def test_edit_comment_not_by_author(self):
        self.client.login(username=self.user2.username,
                          password='my_paSW2')
        comment_id = Comment.objects.get(comment_text="Initial comment").id
        url = reverse('Posts:edit_comment', args=[comment_id])
        response = self.client.post(
            url, {
                'comment_text': 'edited post',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')
        self.assertEquals(Comment.objects.filter(
            comment_text='Initial comment'
        ).count(), 1)
