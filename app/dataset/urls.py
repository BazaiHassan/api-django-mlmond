"""
URL mapping for the recipe app
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from dataset import views

router = DefaultRouter()

router.register('datasets', views.DatasetViewSet)
router.register('tags', views.TagViewSet)


app_name = 'dataset'

urlpatterns = [
    path('', include(router.urls)),
]
