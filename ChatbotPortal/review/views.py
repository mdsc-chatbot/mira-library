from django.shortcuts import render
from .models import Reviews
from .reviewSerializer import ReviewSerializer
from rest_framework import generics, viewsets

# Create your views here.
class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()

class ReviewResource(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()