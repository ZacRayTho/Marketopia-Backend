from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import CustomUser
from rest_framework import mixins

from .serializers import *

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# ------------------MESSAGE VIEWS--------------------------------------------------

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MessageReadSerializer
        else:
            return MessageWriteSerializer

# ------------------REVIEW VIEWS--------------------------------------------------

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewReadSerializer
        else:
            return ReviewWriteSerializer

# ------------------IMAGE VIEWS--------------------------------------------------

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageReadSerializer

# ------------------LOCATION VIEWS--------------------------------------------------

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationReadSerializer