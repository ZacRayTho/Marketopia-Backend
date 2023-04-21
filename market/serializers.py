
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

class UserReadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model =  CustomUser
        fields = ['id', 'first_name', 'last_name']

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
        fields = ['text', 'viewed', 'date_time_sent', 'timestamp', 'sender', 'recipient']




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
    owner = serializers.StringRelatedField()

    class Meta:
        model = Image
        fields = ['id', 'pic', 'owner']

class ImageWriteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Image
        fields = ['id', 'pic', 'owner']

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
    seller = UserReadSerializer()
    location = serializers.StringRelatedField()
    category = CategoryReadSerializer(many=True)
    Image = serializers.StringRelatedField(many=True)

    class Meta:
        model = Listing
        fields = ['id', 'seller', 'location', 'category', 'Image', 'description', 'price', 'title']

class ListingWriteSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    # Image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)

    
    class Meta:
        model = Listing
        fields = ['id', 'seller', 'location', 'category', 'description', 'price', 'title']
