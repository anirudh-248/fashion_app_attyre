from django.core.cache import cache, CacheKeyWarning
import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Video
from .serializers import VideoSerializer
import warnings

class VideoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HomeScreenAPIView(APIView):
    def get(self, request):
        cache_key = f"videos_page_{request.query_params.get('page', 1)}"
        cached_data = None

        # Try to fetch from cache
        try:
            cached_data = cache.get(cache_key)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            warnings.warn("Redis is unavailable, proceeding without caching", CacheKeyWarning)

        # Return cached data if available
        if cached_data:
            return Response(cached_data)

        # Fetch data from the database if cache is unavailable or cache miss
        videos = Video.objects.all()
        paginator = VideoPagination()
        paginated_videos = paginator.paginate_queryset(videos, request)
        serializer = VideoSerializer(paginated_videos, many=True)

        pagination_data = {
            'page': paginator.page.number,
            'limit': paginator.page_size,
            'total_pages': paginator.page.paginator.num_pages,
            'total_videos': paginator.page.paginator.count,
            'next_cursor': paginator.get_next_link()
        }

        response_data = {
            'videos': serializer.data,
            'pagination': pagination_data
        }

        # Try to store data in cache
        try:
            cache.set(cache_key, response_data, timeout=60*10)  # Cache for 10 minutes
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            warnings.warn("Failed to cache data due to Redis unavailability", CacheKeyWarning)

        # Return the response
        return paginator.get_paginated_response(response_data)
