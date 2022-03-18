from . import views
from django.urls import path

urlpatterns = [
    path('detail/<int:id>/<str:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<str:slug>/', views.ArticlesByCategory.as_view(), name='articles_by_category'),
    path('', views.ArticleListView.as_view(), name='articles'),
    path('tag/<str:slug>/', views.ArticlesByTag.as_view(), name='articles_by_tag')
]