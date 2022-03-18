from .models import Product
from rest_framework import serializers
from utilties.drf import ParameterisedHyperlinkedIdentityField


class ProductListSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(
        view_name='product_detail',
        lookup_fields=(('pk', 'id'), ('slug', 'slug')),
        read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'image', 'title', 'price', 'url', 'root_category', 'is_discounted', 'discount_percent')
