from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from campaigns.models import Campaign, Category
from donations.models import Donation
from accounts.models import UserProfile

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image', 'phone_number')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('id', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class CampaignSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    progress_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = ('id', 'title', 'description', 'creator', 'creator_name', 
                  'category', 'category_name', 'goal_amount', 'current_amount', 
                  'image', 'end_date', 'is_featured', 'is_active', 
                  'created_at', 'updated_at', 'progress_percentage', 'days_remaining')
        read_only_fields = ('id', 'creator', 'current_amount', 'is_featured', 
                            'created_at', 'updated_at')
    
    def get_creator_name(self, obj):
        return obj.creator.get_full_name() or obj.creator.username
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def create(self, validated_data):
        # Set creator to current user
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class DonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.SerializerMethodField()
    campaign_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Donation
        fields = ('id', 'campaign', 'campaign_title', 'donor', 'donor_name', 
                  'amount', 'message', 'anonymous', 'simulated_payment_status', 'created_at')
        read_only_fields = ('id', 'donor', 'simulated_payment_status', 'created_at')
    
    def get_donor_name(self, obj):
        if obj.anonymous:
            return "Anonymous"
        if obj.donor:
            return obj.donor.get_full_name() or obj.donor.username
        return "Guest"
    
    def get_campaign_title(self, obj):
        return obj.campaign.title
    
    def create(self, validated_data):
        # Set donor to current user if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        
        # Auto-complete the donation for demo purposes
        validated_data['simulated_payment_status'] = 'completed'
        
        return super().create(validated_data)