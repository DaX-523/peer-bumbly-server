from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from bumbly.models import User as CassandraUser
from django.contrib.auth.models import User as DjangoUser
from bumbly.utils.validation import signup_validation, login_validation, forgot_password_validation, reset_password_validation
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from bumbly.cassandra_connector import get_session
from datetime import datetime

class Home(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def get(self, request):
    return Response({"message" : "Hello, World!"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
  data = request.data
  validation_error = signup_validation(data)
  if validation_error:
    return Response({"error" : validation_error}, status=status.HTTP_400_BAD_REQUEST)
  else :
    # Hash the password before storing
    hashed_password = make_password(data.get("password"))
    
    # Check if user exists in Django
    existing_django_user = DjangoUser.objects.filter(email=data.get("email")).first()
    if existing_django_user:
      return Response({"error" : "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create Django user first
    django_user = DjangoUser.objects.create(
        username=data.get("email"),  # Use email as username
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        password=hashed_password
    )
    
    # Create Cassandra user with same ID
    cassandra_user = CassandraUser()
    cassandra_user.id = django_user.id  # Use Django user's ID
    cassandra_user.first_name = data.get("first_name")
    cassandra_user.last_name = data.get("last_name")
    cassandra_user.email = data.get("email")
    cassandra_user.password = hashed_password
    cassandra_user.age = data.get("age")
    cassandra_user.gender = data.get("gender")
    cassandra_user.created_at = datetime.now()
    cassandra_user.updated_at = datetime.now()
    cassandra_user.save()
    
    token = RefreshToken.for_user(django_user)
    token.payload.update({"user_id" : django_user.id})  # Use integer ID directly
    
    # Create Response object and set cookies on it
    response = Response({"message" : "User created successfully", "user": {
            "id": django_user.id,
            "first_name": django_user.first_name,
            "last_name": django_user.last_name,
            "email": django_user.email
        }}, status=status.HTTP_201_CREATED)
    
    # Set cookies on the Response object
    response.set_cookie(key="access_token", value=str(token.access_token), httponly=True,  samesite="Lax")
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
  data = request.data
  validation_error = login_validation(data)
  if validation_error:
    return Response({"error" : validation_error}, status=status.HTTP_400_BAD_REQUEST)
  else :
    django_user = DjangoUser.objects.filter(email=data.get("email")).first()
    if django_user and check_password(data.get("password"), django_user.password):
      token = RefreshToken.for_user(django_user)
      token.payload.update({"user_id" : django_user.id})  # Use integer ID directly
      
      # Create Response object and set cookies on it
      response = Response({"message" : "Login successful"}, status=status.HTTP_200_OK)
      
      # Set cookies on the Response object
      response.set_cookie(key="access_token", value=str(token.access_token), httponly=True,  samesite="Lax")
      
      return response
    else:
      return Response({"error" : "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
  # Clear cookies
  response = Response({"message" : "Logout successful"}, status=status.HTTP_200_OK)
  response.delete_cookie("access_token")
  response.delete_cookie("refresh_token")
  return response

