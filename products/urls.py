from django.urls import path
from . import views
urlpatterns = [
    path('<int:id>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('all_products/', views.ProductListView.as_view(), name='products'),
    path('product_category/<slug>/', views.ProductsByCategoryView.as_view(), name='products_category'),
    path('product_tag/<slug>/', views.ProductsByTag.as_view(), name='products_tag'),
    path('search/', views.ProductSearchApiView.as_view(), name='products_search'),
    path('compare/', views.ProductCompareView.as_view(), name='products_compare'),
    path('collection/<str:collection_slug>/', views.ProductsByCollection.as_view(), name='products_collection'),
    path('search_redirect/', views.ProductSearchRedirect.as_view(), name='search_redirect'),
    path('search/<category>/<product_name>/', views.ProductSearchByNameView.as_view(), name='products_search_by_name'),
    path(
        'add_or_remove_favorites/',
        views.AddOrRemoveFromFavorites.as_view(),
        name='add_or_remove_favorites'
    ),
    path('favorites/', views.FavoriteProductView.as_view(), name='favorite_products')
]