from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Avg
from users.validators import UsernameValidator


class User(AbstractUser):

    class UserRoles(models.TextChoices):
        USR = 'user', ('User')
        MOD = 'moderator', ('Moderator')
        ADM = 'admin', ('Admin')

    username_validator = UsernameValidator()
    username = models.CharField('Никнейм', max_length=100, unique=True, )
    email = models.EmailField('Почта', max_length=100,
                              unique=True, blank=False,)
    first_name = models.CharField('Имя', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    bio = models.TextField('История пользователя', max_length=1000, blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USR,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    @property
    def is_user(self):
        return self.role == self.UserRoles.USR

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MOD

    @property
    def is_admin(self):
        return self.role == (self.UserRoles.ADM
                             or self.is_superuser
                             or self.is_staff)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ('-username', )

    objects = UserManager()


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Ссылка', max_length=50)

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Ссылка', max_length=50)

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(Category, related_name="title",
                                 on_delete=models.PROTECT, null=True)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Название'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Отзывы на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Ревью'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title_id',),
                name='unique_review'
            )
        ]

    def __str__(self) -> str:
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.score_avg = Review.objects.filter(title_id=self.title).aggregate(
            Avg('score')
        )
        self.title.rating = self.score_avg['score__avg']
        self.title.save()


class Comment(models.Model):
    """Комментарии на отзывы к произведениям."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарии_произведений'

    def __str__(self) -> str:
        return self.text
