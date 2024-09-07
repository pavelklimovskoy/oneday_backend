from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    salary = models.IntegerField(default=0)
    description = models.TextField()

    responsibilities = models.ManyToManyField('Responsibility')
    conditions = models.ManyToManyField('Conditions')
    requirements = models.ManyToManyField('Requirements')


class Responsibility(models.Model):
    title = models.CharField(max_length=256)


class Conditions(models.Model):
    title = models.CharField(max_length=256)


class Requirements(models.Model):
    title = models.CharField(max_length=256)
