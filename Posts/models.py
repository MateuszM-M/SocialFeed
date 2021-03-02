from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Post(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Hidden', 'Hidden')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='posts_created',
                             on_delete=models.CASCADE)
    post_text = models.CharField(max_length=500)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='Published')
    slug = models.SlugField(max_length=200,
                            blank=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        db_index=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.post_text[:20]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_text[:20])
        super(Post, self).save(*args, **kwargs)

    def total_likes_count(self):
        self.total_likes = self.users_like.all().count()
        self.save()


class Comment(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Hidden', 'Hidden')
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    comment_text = models.CharField(max_length=500)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='Published')
    created_date = models.DateTimeField(auto_now_add=True,
                                        db_index=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.comment_text[:20]
