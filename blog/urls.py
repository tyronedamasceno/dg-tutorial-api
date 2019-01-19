from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api/', include(router.urls))
]
