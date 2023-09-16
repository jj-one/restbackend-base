from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

from rest_framework import mixins
from rest_framework import generics

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class PostsGenericAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

  serializer_class = PostSerializer
  queryset = Post.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    return self.list(request)
  
  def post(self, request):
    return self.create(request)
  

class PostDetailsGenericAPIView(
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):
  
  serializer_class = PostSerializer
  queryset = Post.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get(self, request, pk):
    return self.retrieve(request, pk)
  
  def put(self, request, pk):
    return self.update(request, pk)
  
  def delete(self, request, pk):
    return self.destroy(request, pk)
  



class PostsAPIView(APIView):

  def get(self, request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class PostDetailsAPIView(APIView):

  def get_object(self, pk):
    try:
      return Post.objects.get(id=pk)
    except Post.DoesNotExist as _:
      raise Http404
    
  def get(self, request, pk):
    post = self.get_object(pk)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def put(self, request, pk):
    post = self.get_object(pk)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, pk):
    post = self.get_object(pk)
    post.delete()
    return Response(status=status.HTTP_200_OK)


# Create your views here.

@api_view(["GET", "POST"])
def posts_view(resquest):
  if resquest.method == "GET":
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  elif resquest.method == "POST":
    serializer = PostSerializer(data=resquest.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
@api_view(["GET", "PUT", "DELETE"])
def posts_detail(request, pk):
  try:
    post = Post.objects.get(id=pk)
  except Post.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == "GET":
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == "PUT":
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == "DELETE":
    post.delete()
    return Response(status=status.HTTP_200_OK)
  return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
