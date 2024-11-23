from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token   
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view
from .models import CustomUser
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login(request):
    # Check if the user is authenticated
    user = get_object_or_404(CustomUser, email= request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token , created = Token.objects.get_or_create(user=user)
    serializer = CustomUserSerializer(instance=user)
    return Response({'user': serializer.data})

@api_view(['POST'])
def signup(request):
    # Deserialize the incoming data
    serializer = CustomUserSerializer(data=request.data)
    
    # Check if the data is valid
    if serializer.is_valid():
        # Save the user instance (without setting the password yet)
        user = serializer.save()

        # Set the user's password after user creation
        user.set_password(request.data['password'])

        # Save the user with the hashed password
        user.save()

        # Create a token for the saved user
        token = Token.objects.create(user=user)

        # Return the response with the token and user data
        return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)

    # Return errors if serializer is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
