from django.conf.urls import url
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('challenge', views.ChallengeListView.as_view(), name='challenge-list'),
    path('project/by-category/<slug:slug>', views.ProjectByCategoryListView.as_view(), name='project-list-by-category'),
    path('project/by-challenge/<slug:title>', views.ProjectByChallengeListView.as_view(), name='project-list-by-challenge'),
]
