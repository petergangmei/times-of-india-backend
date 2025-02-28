from rest_framework import serializers
from app.models import Article, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'is_published',
            'cover_image', 'author', 'category',
            'location', 'created_at'
        ]
        read_only_fields = ['slug']
