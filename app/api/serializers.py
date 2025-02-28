from rest_framework import serializers
from app.models import Article, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'is_published',
            'cover_image', 'cover_image_url', 'author', 'category',
            'location', 'created_at'
        ]
        read_only_fields = ['slug']
        
    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.cover_image.url)
        return None
