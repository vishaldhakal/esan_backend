from rest_framework import serializers
from .models import  Article, ArticleCategory, Comment, Tag
from account.serializers import UserProfileSerializer
class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ('category_name',)

class ArticleSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('thumbnail_image','title','slug','created_at','thumbnail_image_alt_description','is_featured','is_published','author')
        ordering = ['-created_at']

class ArticleDetailSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','replies','body','created_at','user')

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None