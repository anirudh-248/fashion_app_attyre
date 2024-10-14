from django.db import models
from django.contrib.auth.models import User

# Profile model extending User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.URLField()
    bio = models.TextField()
    followers_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Store model
class Store(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField()

    def __str__(self):
        return self.name
    
# Variant model
class Variant(models.Model):
    name = models.CharField(max_length=255)
    options = models.JSONField()

    def __str__(self):
        return f"{self.name}: {', '.join(self.options)}"

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField()
    image_url = models.URLField()
    timestamp = models.IntegerField()
    currency = models.CharField(max_length=10)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    variants = models.ManyToManyField(Variant, related_name='products')

    def __str__(self):
        return self.name
    
# Music model
class Music(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cover_url = models.URLField()

    def __str__(self):
        return self.name

# Video model
class Video(models.Model):
    video_url = models.URLField()
    thumbnail_url = models.URLField()
    description = models.TextField()
    view_count = models.IntegerField(default=0)
    duration = models.IntegerField()  # Duration in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    hashtags = models.JSONField()

    def __str__(self):
        return f"Video {self.id} by {self.user.username}"
