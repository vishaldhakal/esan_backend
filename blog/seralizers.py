from rest_framework import serializers
from .models import  Articles, Tag

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Articles
        fields = '__all__'

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = 'slug'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Tag
        fields = '__all__'

    