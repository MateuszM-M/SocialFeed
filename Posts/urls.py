from django.urls import path
from . import views



app_name='Posts'
urlpatterns = [
    path('u/<str:username>/<str:pk>/<str:slug>', views.post_view, name='post_view'),
    path('edit/<str:pk>', views.edit_post, name='edit_post'),
    path('delete/<str:pk>', views.delete_post, name='delete_post'),
    path('like/<int:pk>', views.like_post, name='like_post')
    
]