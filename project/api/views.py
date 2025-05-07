from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .serializers import (
    UserCreateSerializer, LoginSerializer, UserSerializer,
    CategorySerializer, CampaignSerializer, DonationSerializer
)
from campaigns.models import Campaign, Category
from donations.models import Donation
from .permissions import IsOwnerOrReadOnly

class RegisterAPIView(generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Log in the user
        login(request, user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    """API endpoint for user login"""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Generate or get existing token
            token, created = Token.objects.get_or_create(user=user)
            
            # Log in the user (create Django session)
            login(request, user)
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint for user profile retrieval and update"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for categories (read-only)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CampaignViewSet(viewsets.ModelViewSet):
    """API endpoint for campaigns"""
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = Campaign.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by creator (user's campaigns)
        creator = self.request.query_params.get('creator')
        if creator:
            queryset = queryset.filter(creator_id=creator)
        
        # Filter by featured status
        featured = self.request.query_params.get('featured')
        if featured:
            featured_bool = featured.lower() == 'true'
            queryset = queryset.filter(is_featured=featured_bool)
        
        # Filter by active status
        active = self.request.query_params.get('active')
        if active:
            active_bool = active.lower() == 'true'
            queryset = queryset.filter(is_active=active_bool)
        
        return queryset

class DonationViewSet(viewsets.ModelViewSet):
    """API endpoint for donations"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Donation.objects.filter(simulated_payment_status='completed').order_by('-created_at')
        
        # Filter by campaign
        campaign = self.request.query_params.get('campaign')
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        
        # Filter by donor (user's donations)
        if self.request.user.is_authenticated:
            user_donations = self.request.query_params.get('user_donations')
            if user_donations and user_donations.lower() == 'true':
                queryset = queryset.filter(donor=self.request.user)
        
        return queryset