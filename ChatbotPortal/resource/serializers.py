from rest_framework import serializers
from .models import Resource, Tag

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class RetrieveResourceSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Resource
        fields = '__all__'

class ResourceUpdateSerializer(serializers.Serializer):
    review_status = serializers.CharField(max_length=50, default="pending")
    rating = serializers.IntegerField(default=1)

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance

class TagUpdateSerializer(serializers.Serializer):
    approved = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TagReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'approved']