from rest_framework import serializers

from .models import *

#TODO Добавит фунцкию, которая будет проверять на суперпользователя

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'