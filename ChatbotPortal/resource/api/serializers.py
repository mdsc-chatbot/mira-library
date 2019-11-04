from rest_framework import serializers

from resource.models import Resource


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

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceUpdateSerializer(serializers.Serializer):
    review_score = serializers.IntegerField(default=0)
    number_of_reviews = serializers.IntegerField(default=0)
    final_review = serializers.CharField(max_length=50, default="pending")

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance