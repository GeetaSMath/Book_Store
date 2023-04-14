from rest_framework import serializers
from user.models import User
from .models import Book


class AllBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'price', 'quantity', 'user']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'price', 'quantity', 'user']
        required_field = ['author', 'title', 'price', 'quantity', "user"]
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
