from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4


# Create your models here.

class Project(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name="Категория")
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    type_pay = models.PositiveSmallIntegerField(choices=((0, 'Расход'), (1, 'Доход')), default=0)

    def __str__(self):
        return self.name  # + " | " + self.get_type_pay_display()

    # class Meta:
    #    ordering = ['name', 'type_pay']


class Operation(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=128, verbose_name="Описание", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория",
                                 related_name='operations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')

    def __str__(self):
        return f'{self.value} | {self.category} | {self.date}'

    # class Meta:
    # ordering = ['-date', '-id']


class Family(models.Model):
    name = models.CharField(max_length=32, verbose_name="Семья")
    author = models.ForeignKey(User, verbose_name='Создатель', blank=True, null=True, on_delete=models.CASCADE,
                               related_name='author_families')
    uuid = models.UUIDField(default=uuid4, editable=True)
    users = models.ManyToManyField(User, blank=True, related_name='family')

    def __str__(self):
        return self.name
