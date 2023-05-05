from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import (Category, Comment, Genre, Review,
                            Title, User)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True, read_only=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        if (
            Review.objects.filter(
                author=self.context.get('request').user,
                title_id=self.context.get('view').kwargs.get('title_id')
            ).exists()
            and self.context.get('request').method == 'POST'
        ):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'text': {'required': True}}


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=100,
                                      regex=r'^[\w.@+-]+\Z', required=True,)

    class Meta:
        fields = (
            'username', 'bio', 'email', 'role', 'first_name', 'last_name',
        )
        model = User

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Такая почта уже используется.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Такой никнейм уже используется.")
        return value


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    username = serializers.RegexField(max_length=100,
                                      regex=r'^[\w.@+-]+\Z', required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Нельзя использовать логин me')
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=100,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
