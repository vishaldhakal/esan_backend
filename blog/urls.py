from imp import get_tag
from django.urls import path
from .views import article_category_detail, article_detail, create_article, create_article_category, create_tag, delete_article, delete_tag, featured_articles, get_category_tag, popular_articles, retrive_articles, retrive_articles_author, update_article, update_article_category, update_tag
urlpatterns = [
    path('create-article-category/', create_article_category, name = 'create_article_category'),
    path('update-article-category/<int:category_id>/', update_article_category, name = 'update_article_category'),
    path('delete-article-category/<int:category_id>/', delete_article, name = 'delete_articles'),
    path('article-category-tags/', get_category_tag, name = 'get_article_category_and_tags'),
    path('article-category/<str:slug>/', article_category_detail, name = 'article_category_details'),
    path('create-article/', create_article, name = 'create_articles'),
    path('update-article/', update_article, name = 'update_articles'),
    path('delete-article/', delete_article, name = 'delete_articles'),
    path('articles/', retrive_articles, name = 'get_articles'),
    path('articles-author/', retrive_articles_author, name = 'get_articles_author'),
    path('create-tag/', create_tag, name = 'create_tag'),
    path('update-article/<int:tag_id>/', update_tag, name = 'update_tag'),
    path('delete-article/<int:tag_id>/', delete_tag, name = 'delete_tags'),
    path('tags/', get_tag, name = 'get_tags'),
    path('article/', article_detail, name = 'article_details'),
    path('featured_articles/', featured_articles, name = 'featured_articles'),
    path('popular_articles/', popular_articles, name = 'popular_articles')
]
