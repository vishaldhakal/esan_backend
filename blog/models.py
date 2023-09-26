from django.db import models
from ckeditor.fields import RichTextField
from account.models import BlogWriter,UserProfile
    
class ArticleCategory(models.Model):
    category_name = models.CharField(max_length=50, help_text='Artcile Category Name')
    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name

class Article(models.Model):
    slug = models.SlugField(unique=True)
    thumbnail_image = models.ImageField(blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    article_content = RichTextField(max_length=500) 
    categories = models.ManyToManyField(ArticleCategory, help_text='Article Category',related_name="categories")
    author = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,related_name="author")
    tags = models.ManyToManyField(Tag,related_name="tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(max_length=400)

    def __str__(self):
        return f'{self.title}'
    class Meta:
        ordering = ['-created_at']

    
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,related_name="user")
    body = models.TextField(blank=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article}' 