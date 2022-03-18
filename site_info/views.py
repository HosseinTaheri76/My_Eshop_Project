from django.views.generic import TemplateView
from products.models import Product, ProductCollection
from articles.models import Article

# Create your views here.

class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class RulesView(TemplateView):
    template_name = 'rules.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Product.objects.all()
        context.update({
            'newest_products': qs.order_by('-id')[:4],
            'most_sold': qs.filter(number_sold__gt=0).order_by('-number_sold')[:4],
            'collections': ProductCollection.objects.all(),
            'articles': Article.objects.order_by('-id')[:4]
        })
        return context
