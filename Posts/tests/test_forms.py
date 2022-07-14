from django.test import SimpleTestCase
from Posts.forms import PostForm, CommentForm


class TestForms(SimpleTestCase):

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'post_text': 'This is my post'
        })

        self.assertTrue(form.is_valid())

    def test_post_form_no_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'comment_text': 'This is my post'
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)