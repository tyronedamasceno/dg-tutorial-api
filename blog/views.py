from django.shortcuts import render

from rest_framework import viewsets

from .serializers import PostSerializer

from .models import Post


# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-title')
    serializer_class = PostSerializer
