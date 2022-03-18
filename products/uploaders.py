def product_img_uploader(instance, filename):
    product_category_repr = instance.category._get_name_path()
    base_path = 'products/' + ('/'.join(name.replace(' ', '_') for name in product_category_repr.split(' / ')))
    return f"{base_path}/{instance.slug}/images/{filename}"


def product_gallery_uploader(instance, filename):
    product_category_repr = instance.product.category._get_name_path()
    base_path = 'products/' + ('/'.join(name.replace(' ', '_') for name in product_category_repr.split(' / ')))
    return f"{base_path}/{instance.product.slug}/images/{filename}"


def collection_cover_uploader(instance, filename):
    return f'products/collections/{instance.slug}/{filename}'
