from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse

# Create your views here.

@csrf_exempt
def posts_view(resquest):
  if resquest.method == "GET":
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)
  
  elif resquest.method == "POST":
    data = JSONParser().parse(resquest)
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  return HttpResponse(status=405)
  
@csrf_exempt
def posts_detail(request, pk):
  try:
    post = Post.objects.get(id=pk)
  except Post.DoesNotExist:
    return HttpResponse(status=404)
  
  if request.method == "GET":
    serializer = PostSerializer(post)
    return JsonResponse(serializer.data)
  elif request.method == "PUT":
    data = JSONParser().parse(request)
    serializer = PostSerializer(post, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  elif request.method == "DELETE":
    post.delete()
    return HttpResponse(status=204)
  return HttpResponse(status=405)
  
