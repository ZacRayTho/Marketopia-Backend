from django.conf import settings
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
# import environ
from django.db.models import Q, F, Max


# env = environ.Env()

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
    serializer_class = UserReadSerializer

class UserPatch(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = UserWriteSerializer


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

class UserChats(APIView):
    def get(self, request, user_id):
        # Get a list of users with whom the current user has communicated
        messages_sent = Message.objects.filter(sender_id=user_id).values('recipient_id').distinct()
        messages_received = Message.objects.filter(recipient_id=user_id).values('sender_id').distinct()
        user_ids = set(messages_sent.values_list('recipient_id', flat=True)) | set(messages_received.values_list('sender_id', flat=True))
        users = CustomUser.objects.filter(id__in=user_ids)

        # Serialize the user ids
        serializer = UserReadSerializer(users, many=True)
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
        print(settings.GOOGLE_MAPS_KEY)
        params = {
            'address': request.data['zip'],
            'key': settings.GOOGLE_MAPS_KEY,
        }

        res = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params=params,
            headers={'Content-Type': 'application/json'}
        )
        data = res.json()
        return JsonResponse(data)
        # Retrieve address components from request data
        city = next((component["long_name"] for component in data["results"][0]["address_components"] if "locality" in component["types"]), None)
        state = next((component["long_name"] for component in data["results"][0]["address_components"] if "administrative_area_level_1" in component["types"]), None)
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        # print(latitude, longitude) 
        zip = request.data['zip']
        # Check if address is already in database

        location, created = Location.objects.get_or_create(city=city, state=state, zip=zip, lat=latitude, long=longitude)
        return JsonResponse({'id': location.id, 'city': location.city, 'state': location.state, 'zip_code': location.zip, 'lat': location.lat, 'long': location.long})

class LocationRange(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationReadSerializer


    def create(self, request, *args, **kwargs):
        print("HERE WE GO")
        print(settings.GOOGLE_MAPS_KEY)
        def get_driving_distance(origin_lat, origin_lng, dest_lat, dest_lng, api_key):
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            params = {
                "units": "imperial",
                "origins": f"{origin_lat},{origin_lng}",
                "destinations": f"{dest_lat},{dest_lng}",
                "key": api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            if data["status"] == "OK":
                distance = data["rows"][0]["elements"][0]["distance"]["value"]
                return distance
            else:
                return None
        # Get user's zip code and range
        user_zip_code = request.data['zip']
        user_range = int(request.data['range'])  # in miles

        # Get user's location from their zip code
        params = {
            'address': user_zip_code,
            'key': settings.GOOGLE_MAPS_KEY,
        }
        res = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params=params,
            headers={'Content-Type': 'application/json'}
        )
        data = res.json()
        user_lat = data["results"][0]["geometry"]["location"]["lat"]
        user_lng = data["results"][0]["geometry"]["location"]["lng"]

        # Loop through all the locations in your database
        nearby_locations = []
        for location in Location.objects.all():
            # Calculate the driving distance between the user's location and the location in your database
            distance = get_driving_distance(user_lat, user_lng, location.lat, location.long, settings.GOOGLE_MAPS_KEY)

            # Convert the distance from meters to miles
            distance = distance * 0.000621371

            # Check if the location is within the user's range
            if distance <= user_range:
                # Add the location to the list of nearby locations
                nearby_locations.append(location)

        # Serialize and return the nearby locations
        serializer = self.get_serializer(nearby_locations, many=True)
        return Response(serializer.data)

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
