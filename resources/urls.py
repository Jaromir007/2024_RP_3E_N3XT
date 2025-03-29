from django.urls import path 
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('blog', views.postlist, name='blog'),
    path('blog/<slug:post_slug>/', views.post, name='post')
]