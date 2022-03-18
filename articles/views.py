from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Article, Category, ArticleTag
from comments.forms import ArticleCommentForm


# Create your views here.

class ArticleDetailView(DetailView):
    model = Article
    pk_url_kwarg = 'id'
    slug_url_kwarg = 'slug'
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        self.get_object().increase_visited()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        sender_fullname = user.full_name if user.is_authenticated else None
        context = super().get_context_data(**kwargs)
        form = ArticleCommentForm(initial=({'sender_fullname': sender_fullname} if sender_fullname else {}))
        context['form'] = form
        return context


class ArticleListView(ListView):
    queryset = Article.objects.order_by('-id')
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 6


class ArticleCategoryPartialView(ListView):
    queryset = Category.objects.filter(parent__isnull=True).order_by('id')
    template_name = 'shared/article_categories.html'
    context_object_name = 'categories'


class ArticlesByCategory(ListView):
    template_name = 'articles.html'
    paginate_by = 6
    context_object_name = 'articles'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=category_slug).get_related_articles()


class ArticlesByTag(ListView):
    template_name = 'articles.html'
    paginate_by = 6
    context_object_name = 'articles'

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        return get_object_or_404(ArticleTag, slug=tag_slug).article_set.order_by('-id')
