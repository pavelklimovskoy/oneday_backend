from django.contrib import admin

from vacancies.models import Vacancy, Responsibility, Conditions, Requirements


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Вакансия'


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Обязанность'


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Условия работы'


@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Требования'

