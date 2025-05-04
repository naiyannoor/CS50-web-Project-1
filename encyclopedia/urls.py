from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:template_name>/", views.entry, name="entry"),
    path("random/", views.rand, name="random"),
    path("create/", views.create, name="create"),
    path("edit/<str:template_name>", views.edit, name="edit"),
]
