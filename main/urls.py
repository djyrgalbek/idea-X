from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import *


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('api/categories/', CategoryListView.as_view()),
    path('api/add-image/', PostImageView.as_view()),
    path('api/', include(router.urls)),
]