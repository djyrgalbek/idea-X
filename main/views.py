from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from .serializers import *
from .permissions import IsPostAuthor, IsOwnerOrReadOnly


class MyPaginationClass(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['text']
            data[i]['text'] = text[:15] + '...'

        return super().get_paginated_response(data)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated, ]
#     pagination_class = MyPaginationClass
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def get_permissions(self):
#         if self.action in ['update', 'partial_update', 'destroy']:
#             permissions = [IsPostAuthor]
#         else:
#             permissions = [IsAuthenticated]
#         return [permission() for permission in permissions]
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         days_count = int(self.request.query_params.get('day', 0))
#         print(days_count)
#         if days_count > 0:
#             start_date = timezone.now() - timedelta(days=days_count)
#             print(start_date)
#             queryset = queryset.filter(created_at__gte=start_date)
#         return queryset
#
#     @action(detail=False, methods=['get'])
#     def own(self, request, pk=None):
#         queryset = self.get_queryset()
#         queryset = queryset.filter(author=request.user)
#         serializer = PostSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#     @action(detail=False, methods=['get'])
#     def search(self, request, pk=None):
#         query = request.query_params.get('query')
#         queryset = self.get_queryset()
#         queryset = queryset.filter(Q(title__icontains=query) |
#                                    Q(text__icontains=query))
#         serializer = PostSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MyPaginationClass

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class SearchListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('query', None)
        # print(len(query))
        if query:
            print('d')
            queryset = queryset.filter(Q(title__icontains=query) |
                                       Q(text__icontains=query))
        elif query is None:
            queryset = ''
        else:
            raise APIException('Параметр пустой')

        return queryset