"""ChatbotPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_profile/', include('user_profile.urls')),
    path('chatbotportal/', include('frontend.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/resource/', include('resource.api.urls')),
    path('', include('review.urls')),
    path('chatbotportal/review/', include('review.urls')),
    path('api/public/', include('public.urls')),

    # For authentication
    path('authentication/', include('authentication.urls')),
    path('chatbotportal/resource/', include('resource.urls')),


    # path to get token, it uses a built in view
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
]
