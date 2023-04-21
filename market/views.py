from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import CustomUser
from rest_framework import mixins
from django.views.decorators.csrf import csrf_exempt
import requests
import environ
from django.db.models import Q


env = environ.Env()

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

class MessageList(APIView):
    def get(self, request, sender_id, recipient_id):
        messages = Message.objects.filter(Q(sender_id=sender_id, recipient_id=recipient_id) | Q(sender_id=recipient_id, recipient_id=sender_id)).order_by('date_time_sent')
        serializer = MessageWriteSerializer(messages, many=True)
        return Response(serializer.data)

# ------------------REVIEW VIEWS--------------------------------------------------

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewReadSerializer
        else:
            return ReviewWriteSerializer

class ReviewFetch(APIView):
    def get(self, request, reviewer, seller):
        review = Review.objects.filter(Q(reviewer=reviewer, seller=seller))
        serializer = ReviewWriteSerializer(review, many=True)
        return Response(serializer.data)

# ------------------IMAGE VIEWS--------------------------------------------------

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ImageReadSerializer
        else:
            return ImageWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the object and get its ID
        self.perform_create(serializer)
        obj_id = serializer.instance.pk
        
        headers = self.get_success_headers(serializer.data)
        
        # Return the ID in the response
        response_data = {
            'id': obj_id,
            **serializer.data,
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

# ------------------LOCATION VIEWS--------------------------------------------------

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationReadSerializer

    def create(self, request, *args, **kwargs):
        print(request.data['zip'])
        params = {
            'address': request.data['zip'],
            'key': env("GOOGLE_MAPS_KEY"),
        }

        res = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params=params,
            headers={'Content-Type': 'application/json'}
        )
        data = res.json()
        # return JsonResponse(data)
        # Retrieve address components from request data
        city = next((component["long_name"] for component in data["results"][0]["address_components"] if "locality" in component["types"]), None)
        state = next((component["long_name"] for component in data["results"][0]["address_components"] if "administrative_area_level_1" in component["types"]), None)
        zip = request.data['zip']
        # Check if address is already in database

        location, created = Location.objects.get_or_create(city=city, state=state, zip=zip)
        return JsonResponse({'id': location.id, 'city': location.city, 'state': location.state, 'zip_code': location.zip})

# ------------------LISTING VIEWS--------------------------------------------------

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListingReadSerializer
        else:
            return ListingWriteSerializer

# ------------------REVIEW VIEWS--------------------------------------------------

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
