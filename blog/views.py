from django.shortcuts import render
from rest_framework.response import Response
from .seralizers import ArticleCategorySerializer, ArticleSerializer, CommentSerializer, TagSerializer,ArticleDetailSerializer
from .models import Article, ArticleCategory, Comment, Tag
from account.models import BlogWriter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.shortcuts import get_object_or_404
from account.models import UserProfile
from django.db.models import Q
from rest_framework import status



@api_view(['POST'])
def create_article_category(request):
    category_name = request.data.get('category_name')
    # Create a new ArticleCategory instance
    category = ArticleCategory(
        category_name=category_name,
    )
    category.save()

    return Response({'success': "Successfully created Article Category"})

@api_view(['PUT'])
def update_article_category(request, category_id):
    category = get_object_or_404(ArticleCategory, id=category_id)
    category_name = request.data.get('category_name')
    category.category_name = category_name
    category.save()

    return Response({'success': "Successfully updated Article Category"})

@api_view(['DELETE'])
def delete_article_category(request, category_id):
    category = get_object_or_404(ArticleCategory, id=category_id)
    category.delete()
    return Response({'success': "Successfully deleted Article Category"})

@api_view(['GET'])
def get_category_tag(request):
    category = ArticleCategory.objects.all()
    category_serializers = ArticleCategorySerializer(category, many=True)
    tag = Tag.objects.all()
    tag_serializers = TagSerializer(tag, many=True)
    return Response({"categories":category_serializers.data,"tags":tag_serializers.data})

@api_view(['GET'])
def article_category_detail(request, slug):
    article_category = ArticleCategory.objects.get(slug=slug)
    serializer = ArticleCategorySerializer(article_category)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_article(request):
    slug = request.POST.get('slug')
    thumbnail_image = request.FILES.get('thumbnail_image')
    thumbnail_image_alt_description = request.POST.get('thumbnail_image_alt_description')
    title = request.POST.get('title')
    article_content = request.POST.get('article_content')
    author_id = request.user.id
    tags = request.POST.getlist('tags')
    categories = request.POST.getlist('categories')
    is_featured = request.POST.get('is_featured',"False")=="True"
    is_published = request.POST.get('is_published',"False")=="True"
    meta_title = request.POST.get('meta_title')
    meta_description = request.POST.get('meta_description')

    # Retrieve the author instance
    author = get_object_or_404(UserProfile, id=author_id)

    # Create a new article instance
    article = Article(
        slug=slug,
        thumbnail_image=thumbnail_image,
        thumbnail_image_alt_description=thumbnail_image_alt_description,
        title=title,
        article_content=article_content,
        author=author,
        is_featured=is_featured,
        is_published =is_published, 
        meta_title=meta_title,
        meta_description=meta_description
    )
    article.save()
    print(thumbnail_image)

    # Retrieve all existing tags
    existing_tags = Tag.objects.filter(Q(tag_name__in=tags))

    # Create new tags for any missing tags
    missing_tags = set(tags) - set(existing_tags.values_list('tag_name', flat=True))
    new_tags = [Tag(tag_name=tag_name) for tag_name in missing_tags]
    Tag.objects.bulk_create(new_tags)

    # Add all tags (existing and new) to the article
    tags_to_add = existing_tags.union(Tag.objects.filter(Q(tag_name__in=missing_tags)))
    article.tags.add(*tags_to_add)

    # Retrieve all existing categories
    existing_categories = ArticleCategory.objects.filter(Q(category_name__in=categories))

    # Create new categories for any missing categories
    missing_categories = set(categories) - set(existing_categories.values_list('category_name', flat=True))
    new_categories = [ArticleCategory(category_name=category_name) for category_name in missing_categories]
    ArticleCategory.objects.bulk_create(new_categories)

    # Add all categories (existing and new) to the article
    categories_to_add = existing_categories.union(ArticleCategory.objects.filter(Q(category_name__in=missing_categories)))
    article.categories.add(*categories_to_add)
    

    return Response({'success': "Sucessfully Uploaded Article"})

@api_view(['POST'])
def create_comment(request):
    article_id = request.POST.get('article_id')
    name = request.POST.get('name')
    body = request.POST.get('body')
    parent_comment_id = request.POST.get('parent_comment_id')

    article = get_object_or_404(Article, id=article_id)

    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        comment = Comment(article=article, name=name, body=body, parent_comment=parent_comment)
    else:
        comment = Comment(article=article, name=name, body=body)

    comment.save()

    serializer = CommentSerializer(comment)

    return Response({'success': "Successfully Added Comment", 'comment': serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_article(request):
    # Retrieve the article instance
    article_id = int(request.POST.get('id'))
    article = get_object_or_404(Article, id=article_id)

    # Check if the requesting user is the author of the article
    if request.user != article.author:
        return Response({'error': 'You do not have permission to update this article.'}, status=status.HTTP_403_FORBIDDEN)

    # Update the article fields
    article.slug = request.POST.get('slug', article.slug)
    article.thumbnail_image = request.FILES.get('thumbnail_image', article.thumbnail_image)
    article.thumbnail_image_alt_description = request.POST.get('thumbnail_image_alt_description', article.thumbnail_image_alt_description)
    article.title = request.POST.get('title', article.title)
    article.article_content = request.POST.get('article_content', article.article_content)
    article.is_featured = request.POST.get('is_featured', article.is_featured)
    article.is_published = request.POST.get('is_published', article.is_published)
    article.meta_title = request.POST.get('meta_title', article.meta_title)
    article.meta_description = request.POST.get('meta_description', article.meta_description)

    # Retrieve all existing tags
    tags = request.POST.getlist('tags')
    existing_tags = Tag.objects.filter(Q(tag_name__in=tags))

    # Create new tags for any missing tags
    missing_tags = set(tags) - set(existing_tags.values_list('tag_name', flat=True))
    new_tags = [Tag(tag_name=tag_name) for tag_name in missing_tags]
    Tag.objects.bulk_create(new_tags)

    # Add all tags (existing and new) to the article
    tags_to_add = existing_tags.union(Tag.objects.filter(Q(tag_name__in=missing_tags)))
    article.tags.set(tags_to_add)

    # Retrieve all existing categories
    categories = request.POST.getlist('categories')
    existing_categories = ArticleCategory.objects.filter(Q(category_name__in=categories))

    # Create new categories for any missing categories
    missing_categories = set(categories) - set(existing_categories.values_list('category_name', flat=True))
    new_categories = [ArticleCategory(category_name=category_name) for category_name in missing_categories]
    ArticleCategory.objects.bulk_create(new_categories)

    # Add all categories (existing and new) to the article
    categories_to_add = existing_categories.union(ArticleCategory.objects.filter(Q(category_name__in=missing_categories)))
    article.categories.set(categories_to_add)

    article.save()

    return Response({'success': "Sucessfully Updated Article"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_article(request):
    article_slug = request.GET.get("slug")
    article = get_object_or_404(Article, slug=article_slug)

    # Check if the requesting user is the author of the article
    if request.user != article.author:
        return Response({'error': 'You do not have permission to update this article.'}, status=status.HTTP_403_FORBIDDEN)
    
    article.delete()

    return Response({'success': "Sucessfully Deleted Article"})

@api_view(["GET"])
def retrive_articles(request):
    articles = Article.objects.all()
    articles_serializers = ArticleSerializer(articles, many = True)

    return Response({
        "posts" : articles_serializers.data,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrive_articles_author(request):

    user = request.user.id
    user_profile = UserProfile.objects.get(id=user)
    articles = Article.objects.filter(author=user_profile)
    articles_serializers = ArticleSerializer(articles, many = True)

    return Response({
        "posts" : articles_serializers.data,
    })

@api_view(['GET'])
def article_detail(request):
    slug = request.GET.get("slug")
    article = Article.objects.get(slug=slug)
    comments = Comment.objects.filter(article=article,parent_comment__isnull=True)
    serializer = ArticleDetailSerializer(article)
    comments_serializer = CommentSerializer(comments, many=True)
    return Response({'post': serializer.data, 'comments': comments_serializer.data})

@api_view(['GET'])
def featured_articles(request):
    featured_articles = Article.objects.filter(is_featured=True).order_by('-id')[:10]
    serializer = [ArticleSerializer(article).data for article in featured_articles]
    return Response({'featured_articles': serializer})  


@api_view(["GET"])
def popular_articles(request):
    popular_articles = Article.objects.filter(is_popular=True).order_by('-created_at')[:5]
    popular_articles_data = [ArticleSerializer(article).data for article in popular_articles]
    return Response(popular_articles_data)

@api_view(['POST'])
def create_tag(request):
    tag_name = request.data.get('tag_name')
    # Create a new tag instance
    tag = Tag(
        tag_name=tag_name,
        
    )
    tag.save()

    return Response({'success': "Successfully created Tag"})

@api_view(['GET'])
def get_tag(request):
    tag = Tag.objects.all()
    serializers = TagSerializer(tag, many=True)
    return Response(serializers.data)

@api_view(['PUT'])
def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag_name = request.data.get('tag_name')
    
    tag.tag_name = tag_name

    tag.save()
    return Response({'success': "Successfully updated Tag"})

def delete_tag(request, tag_id):
    # Retrieve the article to be deleted
    tag = get_object_or_404(Tag, id=tag_id)

    # Delete the article
    tag.delete()

    return Response({'success': "Sucessfully Deleted Tag"})