from rest_framework import viewsets
from .serializers import ProfileSerializer
from .models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset
