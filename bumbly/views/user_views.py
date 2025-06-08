from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from bumbly.models import User, ConnectionRequest, ConnectionStatusEnum
from rest_framework.permissions import IsAuthenticated, AllowAny
from bumbly.cassandra_connector import get_session


#example for direct query execution
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_pending_requests(request): #from params /:user_id it is received here
  loggedInUser = request.user
  session = get_session()
  try:
    pending_requests = session.execute(f"SELECT * FROM connection_request WHERE to_user_id = '{loggedInUser.id}' AND status = '{ConnectionStatusEnum.INTERESTED.value}'")
    return Response({"pending_requests": pending_requests, "status": status.HTTP_200_OK})
  except Exception as error:
    print(error)
    return Response({"error": "Error fetching pending requests", "status": status.HTTP_500_INTERNAL_SERVER_ERROR})
  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_connections(request):
  loggedInUser = request.user
  session = get_session()
  try:
    connections = session.execute(f"SELECT * FROM connection_request WHERE to_user_id = '{loggedInUser.id}' OR from_user_id = '{loggedInUser.id}'")
    return Response({"connections": connections, "status": status.HTTP_200_OK})
  except Exception as error:
    print(error)
    return Response({"error": "Error fetching connections", "status": status.HTTP_500_INTERNAL_SERVER_ERROR})
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_feed(request):
  loggedInUser = request.user
  session = get_session()
  try:
    user_connections = session.execute(f"SELECT * FROM connection_request WHERE to_user_id = '{loggedInUser.id}' OR from_user_id = '{loggedInUser.id}'")
    #hide these users from feed as they have alrady made request to the logged in user  
    usersToHide = set()
    for connection in user_connections:
        usersToHide.add(connection.from_user_id)
        usersToHide.add(connection.to_user_id)
    feed = session.execute(f"SELECT * FROM user WHERE id NOT IN {[req for req in usersToHide]} AND id != {loggedInUser.id}")
    return Response({"feed": feed, "status": status.HTTP_200_OK})
  except Exception as error:
    print(error)
    return Response({"error": "Error fetching feed", "status": status.HTTP_500_INTERNAL_SERVER_ERROR})