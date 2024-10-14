from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video, Product, Store, Profile, Music, Variant

# Store Serializer
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'logo_url']

# Variant Serializer
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'options']

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'original_price', 'discount_percentage', 'image_url', 'timestamp', 'currency', 'store', 'in_stock', 'variants']

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture_url', 'bio', 'followers_count', 'verified']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

# Music Serializer
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name', 'artist', 'cover_url']

# Video Serializer
class VideoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)
    music = MusicSerializer()

    class Meta:
        model = Video
        fields = ['id', 'video_url', 'thumbnail_url', 'description', 'view_count', 'duration', 'created_at', 'user', 'products', 'likes_count', 'comments_count', 'shares_count', 'is_liked', 'is_bookmarked', 'music', 'hashtags']
