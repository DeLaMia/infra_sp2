from api.permissions import IsAdminOrReadOnly, Reviews_permissions
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleGetSerializer, TitlePostSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Comment, Genre, Review, Title


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (Reviews_permissions,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id).order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        Reviews_permissions,
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review_id=review)

    def get_queryset(self):
        review = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review).order_by('id')


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'name')
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleGetSerializer
        return TitlePostSerializer
