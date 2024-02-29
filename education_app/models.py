from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Student(AbstractUser):
    def has_access(self, product):
        return self.groups.filter(product=product).exists()


class NoAvailableGroupsError(Exception):
    pass


class Product(models.Model):  # создаем модель продукта
    author: str = models.ForeignKey(User, on_delete=models.CASCADE,
                                    verbose_name="Автор")  # создаем автора продукта (кто создал продукт)
    name: str = models.CharField(
        max_length=100, verbose_name="Название"
    )  # создаем название продукта
    start_at: str = models.DateTimeField(
        verbose_name="Начало"
    )  # создаем время начала продукта
    cost: float = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    min_group_users: int = models.PositiveSmallIntegerField(verbose_name="Минимальное количество пользователей")
    max_group_users: int = models.PositiveSmallIntegerField(verbose_name="Максимальное количество пользователей")

    def __str__(self):  # переопределяем метод __str__
        return self.name

    def grant_access(self, user):
        group = self.groups.annotate(group_users_count=models.Count('members')).filter(
            group_users_count__lt=self.max_group_users).order_by('group_users_count').first()
        if not group:
            raise NoAvailableGroupsError('Нет доступных групп. Добавьте новую группу.')
        group.members.add(user)


class Lesson(models.Model):  # создаем модель урока
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    name: str = models.CharField(
        max_length=100, verbose_name="Название"
    )
    link_to_video: str = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return self.name


class Group(models.Model):
    product: Product = models.ForeignKey(Product, related_name="groups", on_delete=models.CASCADE,
                                         verbose_name="Продукт")
    members = models.ManyToManyField(User, related_name='groups', verbose_name="Участники")
    name: str = models.CharField(max_length=100, verbose_name="Название группы")

    def __str__(self):
        return self.group_name
