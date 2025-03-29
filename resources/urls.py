from django.urls import path 
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('blog/', views.postlist, name='blog'),
    path('', RedirectView.as_view(url='blog/')),
    path('blog/<slug:post_slug>/', views.post, name='post')
]