from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from bumbly.models import User, ConnectionRequest, ConnectionStatusEnum 
from bumbly.serializers import UserSerializer, ConnectionRequestSerializer
from bumbly.cassandra_connector import get_session
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
        print("posting", request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TODO
# @api_view(['POST'])
# def create_connection_request(request):
#     connection_request = ConnectionRequest.objects.create(
#         from_user_id=request.data.get("from_user_id"),
#         to_user_id=request.data.get("to_user_id"),
#         status=ConnectionStatusEnum.PENDING
#     )
#     return Response(ConnectionRequestSerializer(connection_request).data, status=status.HTTP_201_CREATED)

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