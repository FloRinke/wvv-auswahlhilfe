from django.db import models
from django.conf import settings

class Challenge(models.Model):
    slug = models.SlugField(max_length=32, unique=True)
    title = models.CharField(max_length=255)

    def __repr__(self):
        return("Challenge(title={})".format(self.title))

    def __str__(self):
        return(self.title)

class SlackChannel(models.Model):
    name = models.CharField(max_length=255)
    
    def __repr__(self):
        return("ClackChannel(name={})".format(self.name))

    def __str__(self):
        return(self.name)


class Category(models.Model):
    slug = models.SlugField(max_length=32, unique=True)
    description = models.CharField(max_length=255)

    def __repr__(self):
        return("Category(slug={}, description={})".format(self.slug, self.description))

    def __str__(self):
        return(self.slug)


class Project(models.Model):
    title = models.CharField(max_length=255)
    challenge = models.ForeignKey(Challenge, on_delete=models.PROTECT)
    problem = models. TextField()
    explanation = models. TextField()
    idea = models.TextField()
    affected = models.TextField()
    stakeholder = models.TextField()
    category = models.ManyToManyField(Category)
    slack = models.ForeignKey(SlackChannel, on_delete=models.PROTECT)

    def __str__(self):
        return(self.title)

class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    value = models.IntegerField()
