from django.urls import path
from . import views


app_name = 'Posts'
urlpatterns = [
    path('add_post/', views.add_post, name='add_post'),
    path('u/<str:username>/<str:pk>/<str:slug>', views.post_view, name='post_view'),
    path('edit/<str:pk>', views.edit_post, name='edit_post'),
    path('delete_post/<str:pk>', views.delete_post, name='delete_post'),
    path('like/<str:pk>', views.like_post, name='like_post'),

    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path('remove_comment/<int:pk>', views.remove_comment, name='remove_comment'),
    path('edit_comment/<int:pk>', views.edit_comment, name='edit_comment'),
]
