from django.urls import path
from . import views

urlpatterns = [
    path('api/review/', views.ReviewListCreate.as_view() ),
    path('',views.ReviewResource),
]