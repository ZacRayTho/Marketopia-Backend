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
        return JsonResponse(data)
        # Retrieve address components from request data
        city = data["results"][0]["address_components"][1]["short_name"]
        state = data["results"][0]["address_components"][2]["short_name"]
        zip = request.data['zip']

        # Check if address is already in database
        if not Location.objects.filter(city=city, state=state, zip=zip).exists():
            # If address is not in database, create a new Address object
            serializer = self.get_serializer(data={ "city": city, "state": state, "zip": zip })
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # If address already exists in database, return error response
            return Response({'success': False, 'message': 'Address already exists'}, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
def create_location(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')



        # Use get_or_create() to check if a Location object with the given data already exists
        location, created = Location.objects.get_or_create(city=city, state=state, zip=zip)

        # Return a JSON response with the Location object data
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
