from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Product, ProductSpecificationValue
from utilties.email_utils import send_fav_product_state_change

@receiver(post_save, sender=Product)
def sync_specs_with_category(sender, instance, created, **kwargs):
    if created or instance.tracker.has_changed('category'):
        if not created:
            instance.specifications.all().delete()
        for spec in instance.category.get_specs():
            print(spec)
            ProductSpecificationValue.objects.create(product=instance, specification=spec)


@receiver(post_save, sender=Product)
def notify_fav_users(sender, instance, created, **kwargs):
    if not created and instance.user_favorites.count() > 0:
        recipient_list = instance.user_favorites.values_list('email', flat=True)
        if instance.tracker.has_changed('stock') and instance.tracker.previous('stock') == 0:
            send_fav_product_state_change(instance.title, 'available', recipient_list)
        if instance.tracker.has_changed('discount_percent') and instance.tracker.previous('discount_percent') == 0:
            send_fav_product_state_change(instance.title, 'discounted', recipient_list)
