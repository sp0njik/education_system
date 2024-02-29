from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Product(models.Model):  # создаем модель продукта
    author: str = models.ForeignKey(User, on_delete=models.CASCADE,
                                    verbose_name="Автор")  # создаем автора продукта (кто создал продукт)
    name: str = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Название"
    )  # создаем название продукта
    start_at: str = models.DateTimeField(
        verbose_name="Начало", null=True, blank=True
    )  # создаем время начала продукта
    cost: float = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):  # переопределяем метод __str__
        return self.name


class Lesson(models.Model):  # создаем модель урока
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    name: str = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Название"
    )
    link_to_video: str = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return self.name


class Group(models.Model):
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    group_name: str = models.CharField(max_length=100, null=True, blank=True, verbose_name="Название группы")
    min_users: int = models.IntegerField(null=True, blank=True, verbose_name="Минимальное количество пользователей")
    max_users: int = models.IntegerField(null=True, blank=True, verbose_name="Максимальное количество пользователей")
    members = models.ManyToManyField(User, related_name='groups', blank=True, verbose_name="Участники")

    def __str__(self):
        return self.group_name
