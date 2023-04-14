
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

# ------------------USER SERIALIZERS--------------------------------------------------

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
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
        fields = '__all__'

# ------------------LOCATION SERIALIZERS--------------------------------------------------

class LocationReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# ------------------LISTING SERIALIZERS--------------------------------------------------

class ListingReadSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)
    image = serializers.StringRelatedField(many=True)

    class Meta:
        model = Listing
        fields = '__all__'

class ListingWriteSerializer(serializers.HyperlinkedModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)

    
    class Meta:
        model = Listing
        fields = '__all__'

# ------------------CATEGORY SERIALIZERS--------------------------------------------------

class CategoryReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'