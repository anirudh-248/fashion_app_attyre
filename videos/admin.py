from django.contrib import admin
from .models import Profile, Store, Product, Video, Music, Variant

# Register your models here.
admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Video)
admin.site.register(Music)
admin.site.register(Variant)