from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from bumbly.models import User
from bumbly.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from bumbly.cassandra_connector import get_session

@api_view(['GET', 'PUT'])  # Allow both GET and PUT methods
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    loggedInUser = request.user
    session = get_session()
    
    try:        
        query = "SELECT * FROM user WHERE id = %s"
        result = session.execute(query, [user_id])
        user = result.one()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
                
            user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'age': user.age if hasattr(user, 'age') else None,
                'gender': user.gender if hasattr(user, 'gender') else None,
                'photo_url': user.photo_url if hasattr(user, 'photo_url') else None,
                'bio': user.bio if hasattr(user, 'bio') else None,
                'location': user.location if hasattr(user, 'location') else None,
                'skills': user.skills if hasattr(user, 'skills') else [],
                'interests': user.interests if hasattr(user, 'interests') else [],
                'education': user.education if hasattr(user, 'education') else [],
                'work': user.work if hasattr(user, 'work') else [],
                'hobbies': user.hobbies if hasattr(user, 'hobbies') else []
            }
            return Response(user_dict, status=status.HTTP_200_OK)
            
        elif request.method == 'PUT':

            # Build update query
            update_fields = []
            update_values = []
            
            for key, value in request.data.items():
                if key in ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']:
                    continue
                if value is not None:  # Only update non-null values
    #                 update_fields = [
                            # "location = %s",
                            # "skills = %s",
                            # "interests = %s"
                        # ]
                    update_fields.append(f"{key} = %s")
                    update_values.append(value)
            
            if not update_fields:
                return Response({"error": "No fields to update"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Add user_id to values
            update_values.append(user_id)
            
            # Construct and execute update query
            update_query = f"UPDATE user SET {', '.join(update_fields)} WHERE id = %s"
            session.execute(update_query, update_values)
            
            return Response({
                "message": "User profile updated successfully",
                "updated_fields": [field.split(' = ')[0] for field in update_fields]
            }, status=status.HTTP_200_OK)
            
    except Exception as error:
        print("Error:", str(error))
        return Response({"error": f"Error with user profile: {str(error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        session.shutdown()
 