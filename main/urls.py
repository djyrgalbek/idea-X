from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import *


router = DefaultRouter()
# router.register('posts', PostViewSet)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    # path('', include(router.urls)),
    path('posts/', PostListView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('search/', SearchListView.as_view()),

]