from django.contrib import admin

from vacancies.models import Vacancy, Responsibility, Conditions, Requirements


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    pass


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    pass


