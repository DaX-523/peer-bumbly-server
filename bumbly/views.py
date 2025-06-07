from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .cassandra_connector import get_session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def users(request):
    print("users", request.data)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# generic views normally used for sql databases
# class UserListCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# cassandra views

def hello(request):
    page = loader.get_template("template1.html")
    return HttpResponse(page.render())