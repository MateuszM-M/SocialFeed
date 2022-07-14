from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Posts.views import *


class TestUrls(SimpleTestCase):

    def test_add_post_url_resolving(self):
        url = reverse('Posts:add_post')
        self.assertEquals(resolve(url).func, add_post)

    def test_post_view_url_resolving(self):
        url = reverse('Posts:post_view', args=['some-user', '1', 'bla-bla-bla'])
        self.assertEquals(resolve(url).func, post_view)

    def test_edit_post_url_resolving(self):
        url = reverse('Posts:edit_post', args=['1'])
        self.assertEquals(resolve(url).func, edit_post)

    def test_delete_post_url_resolving(self):
        url = reverse('Posts:delete_post', args=['8'])
        self.assertEquals(resolve(url).func, delete_post)

    def test_like_post_url_resolving(self):
        url = reverse('Posts:like_post', args=[5])
        self.assertEquals(resolve(url).func, like_post)

    def test_add_comment_url_resolving(self):
        url = reverse('Posts:add_comment', args=[3])
        self.assertEquals(resolve(url).func, add_comment)

    def test_remove_comment_url_resolving(self):
        url = reverse('Posts:remove_comment', args=[10])
        self.assertEquals(resolve(url).func, remove_comment)

    def test_edit_comment_url_resolving(self):
        url = reverse('Posts:edit_comment', args=[10])
        self.assertEquals(resolve(url).func, edit_comment)
