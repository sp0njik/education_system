from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Student(AbstractUser):
    def has_access(self, product):
        # """
        # Проверяет, имеет ли пользователь доступ к определенному продукту
        # параметры:product - продукт для которого проверяется доступ
        # возвращает: True, если пользователь имеет доступ, иначе False
        # """
        return self.groups.filter(product=product).exists()

    def __str__(self):
        name = self.username
        if self.first_name or self.last_name:
            name = f"{self.first_name} {self.last_name}".strip()
        return name


class NoAvailableGroupsError(Exception):
    pass


class Product(models.Model):  # создаем модель продукта
    author: str = models.ForeignKey(Student, on_delete=models.CASCADE,
                                    verbose_name="Автор")  # создаем автора продукта
    name: str = models.CharField(
        max_length=100, verbose_name="Название"
    )  # создаем название продукта
    start_at: str = models.DateTimeField(
        verbose_name="Начало"
    )  # создаем время начала продукта
    cost: float = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")  # создаем стоимость
    min_group_users: int = models.PositiveSmallIntegerField(
        verbose_name="Минимальное количество пользователей")  # создаем минимальное количество пользователей
    max_group_users: int = models.PositiveSmallIntegerField(
        verbose_name="Максимальное количество пользователей")  # создаем максимальное количество пользователей

    @property
    def lessons_count(self):
        return self.lessons.count()

    def __str__(self):
        return self.name

    def grant_access(self, user):
        # '''
        # Предоставляет доступ к группе для указанного пользователя
        # параметры:user - пользователь для которого предоставляется доступ
        # вызывает:NoAvailableGroupsError - если нет доступных групп для пользователя
        #
        # '''
        group = self.groups.annotate(group_users_count=models.Count('members')).filter(
            group_users_count__lt=self.max_group_users).order_by('group_users_count').first()  # выбираем группу
        if not group:
            raise NoAvailableGroupsError('Нет доступных групп. Добавьте новую группу.')
        group.members.add(user)


class Lesson(models.Model):  # создаем модель урока
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lessons",
                                         verbose_name="Продукт")  # создаем продукт урока
    name: str = models.CharField(
        max_length=100, verbose_name="Название"
    )  # создаем название урока
    link_to_video: str = models.URLField(verbose_name="Ссылка на видео")  # создаем ссылку на видео

    def __str__(self):
        return self.name


class Group(models.Model):  # создаем модель группы
    product: Product = models.ForeignKey(Product, related_name="group", on_delete=models.CASCADE,
                                         verbose_name="Продукт")  # создаем продукт группы
    members = models.ManyToManyField(Student, related_name='education_groups',
                                     verbose_name="Участники")  # создаем участников
    name: str = models.CharField(max_length=100, verbose_name="Название группы")  # создаем название группы

    def __str__(self):
        return self.name
