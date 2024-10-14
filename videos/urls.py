from django.urls import path
from .views import HomeScreenAPIView

urlpatterns = [
    path('', HomeScreenAPIView.as_view(), name='home-screen'),
]
