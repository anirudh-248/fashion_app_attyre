from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Video
from .serializers import VideoSerializer

class VideoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HomeScreenAPIView(APIView):
    def get(self, request):
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
        
        return paginator.get_paginated_response({
            'videos': serializer.data,
            'pagination': pagination_data
        })
