from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Challenge, Project

class IndexView(TemplateView):
    template_name = "projects/index.html"


class CategoryListView(ListView):
    model = Category

class ChallengeListView(ListView):
    model = Challenge

class ProjectByCategoryListView(ListView):
    model = Project

class ProjectByChallengeListView(ListView):
    model = Project

