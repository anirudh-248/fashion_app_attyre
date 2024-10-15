from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Video

@receiver(post_save, sender=Video)
def clear_cache_on_save(sender, instance, **kwargs):
    # Clear cache when a new video is added or an existing one is updated
    cache.delete_pattern('videos_page_*')  # Clear all cached video pages

@receiver(post_delete, sender=Video)
def clear_cache_on_delete(sender, instance, **kwargs):
    # Clear cache when a video is deleted
    cache.delete_pattern('videos_page_*')  # Clear all cached video pages
