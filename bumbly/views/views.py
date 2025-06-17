from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from bumbly.models import User, ConnectionRequest, ConnectionStatusEnum, SuperConnectionRequest
from bumbly.serializers import UserSerializer, ConnectionRequestSerializer, SuperConnectionRequestSerializer
from bumbly.cassandra_connector import get_session
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def users(request):
    """
    Retrieve all users (GET) or create a new user (POST).
    - GET: Returns a list of all users.
    - POST: Creates a new user with the provided data.
    No authentication required.
    """
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

#TODO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_connection_request(request):
    """
    Create a new connection request from the logged-in user to another user.
    - POST: Requires authentication.
    - Validates that the user is not sending a request to themselves and that the status is allowed.
    - Prevents duplicate requests.
    """
    loggedInUser = request.user
    request_data = request.data.copy()
    if loggedInUser.id == request_data.get("to_user_id"):
        return Response({"error": "You cannot send a connection request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
    allowed_statues = [ConnectionStatusEnum.INTERESTED.value, ConnectionStatusEnum.IGNORED.value]
    if request_data.get("status") not in allowed_statues:
        return Response({"error": "Invalid status", "status":status.HTTP_400_BAD_REQUEST})
    request_data["from_user_id"] = loggedInUser.id
    existing_request = ConnectionRequest.objects.filter(from_user_id=loggedInUser.id, to_user_id=request_data["to_user_id"]).first()
    if existing_request:
        return Response({"error": "You already have interaction with this user", "status":status.HTTP_400_BAD_REQUEST})
    # connection_request = ConnectionRequest.objects.create(**request_data) normal django orm way
    connection_request = ConnectionRequest() # but we are using cassandra so we do it this way
    connection_request.status = request_data.get("status")
    connection_request.from_user_id = loggedInUser.id
    connection_request.to_user_id = request_data.get("to_user_id")
    connection_request.created_at = datetime.now()
    connection_request.updated_at = datetime.now()
    connection_request.save()
    return Response(ConnectionRequestSerializer(connection_request).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def create_super_connection_request(request):
    """
    Create a new super connection request from the logged-in user to another user.
    - POST: Requires authentication.
    - Validates that the user is not sending a request to themselves.
    - Prevents duplicate super connection requests.
    """
    loggedInUser = request.user
    request_data = request.data.copy()
    if loggedInUser.id == request_data.get("to_user_id"):
        return Response({"error": "You cannot send request to yourself", "status": status.HTTP_400_BAD_REQUEST})
    existing_request = SuperConnectionRequest.objects.filter(from_user_id=request_data.get("from_user_id"), to_user_id=request_data.get("to_user_id")).first()
    if existing_request:
        return Response({"error": "You already have interaction with this user", "status":status.HTTP_400_BAD_REQUEST})
    super_connection_request = SuperConnectionRequest()
    super_connection_request.from_user_id = loggedInUser.id
    super_connection_request.to_user_id = request_data.get("to_user_id")
    super_connection_request.created_at = datetime.now()
    super_connection_request.updated_at = datetime.now()
    super_connection_request.save()
    return Response(SuperConnectionRequestSerializer(super_connection_request).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_or_reject_connection_request(request):
    """
    Accept or reject a connection request as the sender.
    - POST: Requires authentication.
    - Only the sender can accept or reject their own connection requests.
    - Validates status and request existence.
    """
    loggedInUser = request.user
    request_data = request.data.copy()
    allowed_statuses = [ConnectionStatusEnum.ACCEPTED.value, ConnectionStatusEnum.REJECTED.value]
    if request_data.get("status") not in allowed_statuses:
        return Response({"error": "Invalid status", "status":status.HTTP_400_BAD_REQUEST})
    connection_request = ConnectionRequest.objects.filter(from_user_id=loggedInUser.id, id=request_data.get("request_id")).first()
    if not connection_request:
        return Response({"error": "Connection request not found", "status": status.HTTP_404_NOT_FOUND})
    if connection_request.status == ConnectionStatusEnum.IGNORED.value:
        return Response({"error": "You have already ignored this user", "status": status.HTTP_400_BAD_REQUEST})
    if connection_request.from_user_id != loggedInUser.id:
        return Response({"error": "You are not the sender of this connection request", "status": status.HTTP_400_BAD_REQUEST})
    connection_request.status = request_data.get("status")
    connection_request.updated_at = datetime.now()  
    connection_request.save()
    return Response(ConnectionRequestSerializer(connection_request).data, status=status.HTTP_200_OK)
     

# generic views normally used for sql databases
# class UserListCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# cassandra views

def hello(request):
    """
    Render and return the template1.html page.
    No authentication required.
    """
    page = loader.get_template("template1.html")
    return HttpResponse(page.render())