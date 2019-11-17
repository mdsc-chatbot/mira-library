from rest_framework import serializers

from resource.models import Resource, Tag

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RetrievePublicResourceSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Resource
        fields = ['title', 'url', 'rating', 'comments', 'tags', 'attachment', 'timestamp', 'review_status']
