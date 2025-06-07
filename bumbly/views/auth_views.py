from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from bumbly.models import User
from bumbly.utils.validation import signup_validation, login_validation, forgot_password_validation, reset_password_validation
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

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
    existngUser = User.objects.filter(email=data.get("email")).first()
    if existngUser:
      return Response({"error" : "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    newUser = User.objects.create(**data)
    newUser.password = hashed_password
    
    newUser.save()
    
    token = RefreshToken.for_user(newUser)
    print(token)
    token.payload.update({"user_id" : str(newUser.id)})  # Convert UUID to string
    
    # Create Response object and set cookies on it
    response = Response({"message" : "User created successfully", "user": {
            "id": str(newUser.id),
            "first_name": newUser.first_name,
            "last_name": newUser.last_name,
            "email": newUser.email
        }}, status=status.HTTP_201_CREATED)
    
    # Set cookies on the Response object
    # response.set_cookie(key="refresh_token", value=str(token), httponly=True,  samesite="Lax")
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
    user = User.objects.filter(email=data.get("email")).first()
    if user and check_password(data.get("password"), user.password):
      token = RefreshToken.for_user(user)
      token.payload.update({"user_id" : str(user.id)})  # Convert UUID to string
      
      # Create Response object and set cookies on it
      response = Response({"message" : "Login successful"}, status=status.HTTP_200_OK)
      
      # Set cookies on the Response object
      # response.set_cookie(key="refresh_token", value=str(token), httponly=True, secure=True, samesite="Lax")
      response.set_cookie(key="access_token", value=str(token.access_token), httponly=True,  samesite="Lax")
      
      return response
    else:
      return Response({"error" : "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
  return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

