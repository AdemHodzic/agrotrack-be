from rest_framework import generics, permissions
from .models import Plot
from .serializers import PlotSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User 
import logging
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound

class PlotListView(generics.ListAPIView):
    serializer_class = PlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Plot.objects.filter(users=self.request.user)

class PlotDetailView(generics.ListAPIView):
    serializer_class = PlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
        return Plot.objects.filter(users=user)

logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    # Create or get the auth token for the user
                    token, created = Token.objects.get_or_create(user=user)
                    full_name = f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username
                    logger.info(f"User {email} authenticated successfully.")
                    return Response({
                        "message": "Login successful",
                        "full_name": full_name,
                        "token": token.key,
                        "user_id": user.id
                    }, status=status.HTTP_200_OK)
                else:
                    logger.warning(f"Invalid credentials for user {email}.")
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                logger.warning(f"User with email {email} does not exist.")
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)