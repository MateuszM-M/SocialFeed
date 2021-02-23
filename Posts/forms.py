from django.forms import ModelForm, Textarea, TextInput
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_text']
        widgets = {
            'post_text': TextInput(attrs={
                'placeholder': 'Type your post here...',
                'class': 'form-control col-6'
            })
        }
        
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': Textarea(attrs={
                'placeholder': 'Type your comment here...',
                'rows': 2,
                'class': 'form-control ml-5 col-7'
            })
        }
