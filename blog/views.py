from django.shortcuts import render
from rest_framework.response import Response
from .seralizers import ArticleSerializer, TagSerializer
from .models import Articles, Tag
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(["GET"])
def Article(request):
    featured_articles = Articles.objects.filter(is_featured=True)
    featured_articles_serializers = ArticleSerializer(featured_articles, many = True)

    popoular_articles = Articles.objects.filter(is_popular=True)
    popoular_artcles_serializers = ArticleSerializer(popoular_articles, many = True)

    tag = Tag.objects.all()
    tag_serializers = TagSerializer(tag, many = True)
    return Response({
        "featured_articles" : featured_articles_serializers.data,
        "popular_articles" : popoular_artcles_serializers.data,
        "tag" : tag_serializers.data
    })

@api_view(['GET'])
def Article_Detail(request, slug):
    try:
        article_detail = Articles.objects.get(slug=slug)
        article_detail_serializer = ArticleSerializer(article_detail)
        return Response(article_detail_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Featured_Articles(request):
    featured_articles = Articles.objects.filter(is_featured=True).order_by('-id')[:10]
    serializer = [ArticleSerializer(article).data for article in featured_articles]
    return Response(serializer)  

@api_view(["GET"])
def Popular_Articles(request):
    popular_articles = Articles.objects.all().order_by('-created_at')[:5]
    popular_articles_data = [ArticleSerializer(article).data for article in popular_articles]
    return Response(popular_articles_data)