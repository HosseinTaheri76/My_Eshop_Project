from django.urls import path
from .views import CommentCreateView
urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='create_comment'),
]