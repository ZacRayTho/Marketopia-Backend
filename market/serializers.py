
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

# ------------------USER SERIALIZERS--------------------------------------------------

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    # username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# ------------------MESSAGE SERIALIZERS--------------------------------------------------

class MessageReadSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    class Meta:
        model =  Message
        fields = '__all__'

class MessageWriteSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model =  Message
        fields = '__all__'

# ------------------REVIEW SERIALIZERS--------------------------------------------------

class ReviewReadSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = '__all__'

class ReviewWriteSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Review
        fields = '__all__'

# ------------------IMAGE SERIALIZERS--------------------------------------------------

class ImageReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'pic']

# ------------------LOCATION SERIALIZERS--------------------------------------------------

class LocationReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'state', 'zip']

# ------------------CATEGORY SERIALIZERS--------------------------------------------------

class CategoryReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# ------------------LISTING SERIALIZERS--------------------------------------------------

class ListingReadSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    category = CategoryReadSerializer(many=True)
    Image = serializers.StringRelatedField(many=True)

    class Meta:
        model = Listing
        fields = ['id', 'seller', 'location', 'category', 'Image', 'description', 'price', 'title']

class ListingWriteSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    location = LocationReadSerializer()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    Image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)

    
    class Meta:
        model = Listing
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location_id = location_data.get('id')
        if location_id:
            location = Location.objects.get(pk=location_id)
            location_serializer = LocationReadSerializer(instance=location, data=location_data)
            location_serializer.is_valid(raise_exception=True)
            location_serializer.save()
        else:
            location = Location.objects.create(**location_data)
        listing = Listing.objects.create(location=location, **validated_data)
        return listing