from rest_framework import serializers

from resource.models import Resource, Tag, Category

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RetrievePublicResourceSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Resource
        fields = ['id', 'title', 'url', 'rating', 'comments', 'tags', 'attachment', 'timestamp', 'review_status', 'website_summary_metadata']
