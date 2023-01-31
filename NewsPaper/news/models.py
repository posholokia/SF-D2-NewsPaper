from django.contrib.auth.models import User
from django.db import models

from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.SmallIntegerField(default=0)

    def update_rating(self):  # обновление рейтинга автора
        # считаем рейтинг постов автора
        author_post_rating = 0  # изначально рейтинг 0
        # получаем рейтинг всех постов автора из класса Post
        post_rating = self.post_set.all().aggregate(post_rating=Sum('post_rating'))
        # если Постов нет, то получим None и выйдет ошибка при сложении
        if self.post_set.exists():  # проверяем, что посты есть
            # складываем начальный рейтинг и значение ключа из полученного словаря
            author_post_rating += post_rating.get('post_rating')

        # считаем рейтинг комментариев автора
        author_comment_rating = 0
        comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        if self.author.comment_set.exists():  # проверяем, что есть комментарии от автора
            author_comment_rating += comment_rating.get('comment_rating')

        # считаем рейтинг всех комментариев других пользователей под постами автора
        user_comment_rating = 0
        # комментарии связаны с постами, а посты с авторами
        for post in self.post_set.all():  # идем циклом по постам
            # рейтинг всех комментариев под постами, исключая автора поста. Рейтинг комментария автора посчитан выше
            user_rating = post.comment_set.exclude(comment_user=self.author).aggregate(
                all_comment_rating=Sum('comment_rating'))
            if post.comment_set.exclude(comment_user=self.author).exists():  # проверяем, что комментарии к посту есть
                user_comment_rating += user_rating.get('all_comment_rating')

        self.author_rate = author_post_rating * 3 + author_comment_rating + user_comment_rating
        self.save()

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    # задаем выбор типа постов: новость или статья
    news = 'NW'
    article = 'AR'
    POSTS_CHOICES = (
        (news, 'Новость'),
        (article, 'Статья')
    )
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSTS_CHOICES)
    post_date = models.DateField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=64)
    post_text = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:19]}...'

    def __str__(self):
        return f'{self.post_title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    through_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    through_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now_add=True)
    comment_text = models.TextField()
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_user}: {self.comment_post}'



