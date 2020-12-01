from django.shortcuts import render

from rest_framework import generics
from apps.category.models import Category

from .serializers import CategoryAPISerializer

class CategoryApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAPISerializer