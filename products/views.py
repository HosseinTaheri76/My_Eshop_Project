from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, FormView
from rest_framework.generics import ListAPIView
from .models import Product, Category, DefaultSpecificationValue, ProductTag, ProductCollection
from .serializers import ProductListSerializer
from utilties.drf import MyPaginator
from comments.forms import ProductCommentForm
from utilties.messaging import get_message


# Create your views here.

class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    pk_url_kwarg = 'id'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get(self, *args, **kwargs):
        self.get_object().increase_visited()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        show_add_favorite = False
        sender_fullname = user.full_name if user.is_authenticated else None
        context = super().get_context_data(**kwargs)
        form = ProductCommentForm(initial=({'sender_fullname': sender_fullname} if sender_fullname else {}))
        context['form'] = form
        if user.is_authenticated and self.get_object() not in user.favorite_products.all():
            show_add_favorite = True
        context['show_add_favorite'] = show_add_favorite
        return context


class ProductListView(ListView):
    queryset = Product.objects.order_by('-id')
    paginate_by = 6
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductsByCategoryView(ListView):
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_category(self):
        category_slug = self.kwargs['slug']
        return get_object_or_404(Category, slug=category_slug)

    def get_queryset(self):
        return self.get_category().related_products().order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category'] = self.get_category()
        return context


class CategoryListView(ListView):
    template_name = 'shared/category_list.html'
    queryset = Category.objects.filter(parent__isnull=True)
    context_object_name = 'categories'


class ProductCompareView(TemplateView):
    template_name = 'product_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = None
        products_info = self.request.COOKIES.get('compare')
        if products_info:
            product_ids = [int(info.split(':')[0]) for info in products_info.split(',')]
            type_ids = [int(info.split(':')[1]) for info in products_info.split(',')]
            if len(set(type_ids)) == 1:
                qs = Product.make_compare_ready(*Product.objects.filter(id__in=product_ids))
                data = {
                    'head': qs[0],
                    'body': qs[1:]
                }
        context['products'] = data
        return context


class ProductSearchApiView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        query_params = self.request.GET.copy()
        initial = Category.objects.get(id=int(query_params.pop('category_id')[0])).related_products()
        if query_params:
            attr_value = [k.replace('attr', '') for k in query_params if k.startswith('attr')]
            attr_set = set([i.split('-')[0] for i in attr_value])
            attr_values = {int(k): [int(i.split('-')[1]) for i in attr_value if i.startswith(k)] for k in attr_set}
            attr_values = {
                k: DefaultSpecificationValue.objects.filter(id__in=v).values_list('value', flat=True) for k, v in
                attr_values.items()
            }
            for k, v in attr_values.items():
                initial = initial.filter(specifications__specification_id=k, specifications__value__in=v)
        return initial


class ProductsByTag(ListView):
    template_name = 'product_list.html'
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = get_object_or_404(ProductTag, slug=tag_slug)
        return tag.get_related_products().order_by('-id')


class ProductsByCollection(ListView):
    template_name = 'product_list.html'
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('collection_slug')
        collection = get_object_or_404(ProductCollection, slug=slug)
        return Product.objects.filter(category__in=collection.categories.all())


class ProductSearchRedirect(View):
    def get(self, form):
        query_params = self.request.GET
        return redirect('products_search_by_name',
                        query_params['category'] if query_params['category'] else 'all',
                        query_params['product_name']
                        )


class ProductSearchByNameView(ListView):
    paginate_by = 6
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.search(**self.kwargs)


class AddOrRemoveFromFavorites(LoginRequiredMixin, View):
    def post(self, request):
        action_template = {
            'remove': {
                'msg': get_message('products/removed_favorites'),
                'func': Product.delete_from_user_favorites
            },
            'add': {
                'msg': get_message('products/added_favorites'),
                'func': Product.add_user_to_favorites
            }
        }
        data = request.POST
        product_id = int(data['product_id'])
        action = data['action']
        product = get_object_or_404(Product, id=product_id)
        result = action_template[action]['func'](product, request.user)
        msg = ('SUCCESS', action_template[action]['msg'].format(product.title)) if result else (
            'ERROR', 'متاسفانه مشکلی پیش آمد.')
        messages.add_message(request, getattr(messages, msg[0]), msg[1])
        return redirect(request.META['HTTP_REFERER'])


class FavoriteProductView(LoginRequiredMixin, TemplateView):
    template_name = 'favorite_products.html'
