def article_image_uploader(instance, filename):
    path = instance.category._get_name_path('slug').replace(' ', '')
    return f'articles/{path}/{instance.title}/image/{filename}'
