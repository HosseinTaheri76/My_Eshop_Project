from django.urls import path
from . import views
urlpatterns = [
    path('about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('rules/', views.RulesView.as_view(), name='rules'),
]