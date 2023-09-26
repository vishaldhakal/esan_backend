from django.contrib import admin
from . models import ArticleCategory, Article, Tag, Comment
# Register your models here.

admin.site.register(ArticleCategory)
admin.site.register(Tag)
admin.site.register(Comment)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "is_featured",
        "is_published",
        "updated_at",
    )
    list_filter = ("updated_at", "is_published","is_featured")


admin.site.register(Article, ArticleAdmin)