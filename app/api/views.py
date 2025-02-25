from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Article.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__iexact=location)
        
        # Filter by published status
        is_published = self.request.query_params.get('is_published', None)
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == 'true')
        
        return queryset

    @action(detail=True, methods=['get'])
    def detail(self, request, slug=None):
        try:
            article = self.get_object()
            
            # Get related articles from the same category
            related_articles = Article.objects.filter(
                category=article.category,
                is_published=True
            ).exclude(id=article.id)[:5]  # Get 5 related articles
            
            # Serialize the data
            article_data = ArticleSerializer(article).data
            related_articles_data = ArticleSerializer(related_articles, many=True).data
            
            return Response({
                'article': article_data,
                'related_articles': related_articles_data
            })
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=404)
