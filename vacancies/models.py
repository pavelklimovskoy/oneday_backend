from django.db import models


class Responsibility(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Обязанность'
        verbose_name_plural = 'Обязанности'

    def __str__(self):
        return f'Название обязанности: {self.title}'


class Conditions(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Условия работы'
        verbose_name_plural = 'Условия работы'

    def __str__(self):
        return f'Название условия работы: {self.title}'


class Requirements(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Требование'
        verbose_name_plural = 'Требования'

    def __str__(self):
        return f'Название требование: {self.title}'


class Vacancy(models.Model):
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Отображать в списке'
    )

    title = models.CharField(
        max_length=256,
        verbose_name='Название вакансии',
        unique=True,
        primary_key=True
    )
    address = models.CharField(
        max_length=256,
        verbose_name="Адрес работы"
    )
    salary = models.IntegerField(
        default=0,
        verbose_name='Зарплата'
    )
    description = models.TextField(
        verbose_name='Описание вакансии'
    )

    responsibilities = models.ManyToManyField(
        Responsibility,
        verbose_name='Обязанности',
        null=True,
        blank=True
    )
    conditions = models.ManyToManyField(
        Conditions,
        verbose_name='Условия работы',
        null=True,
        blank=True
    )
    requirements = models.ManyToManyField(
        Requirements,
        verbose_name='Требования',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return f'Вакансия {self.title}'
