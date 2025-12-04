from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, RecruiterProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'profile_picture')
        read_only_fields = ('id', 'role')  # Role should not be changeable after registration

class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CandidateProfile
        fields = '__all__'

class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = RecruiterProfile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.UserRole.choices)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'role')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role']
        )
        
        # Create corresponding profile based on role
        if user.role == User.UserRole.CANDIDATE:
            CandidateProfile.objects.create(user=user)
        elif user.role == User.UserRole.RECRUITER:
            RecruiterProfile.objects.create(user=user)
            
        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # We do NOT set username_field = User.EMAIL_FIELD here because that would make the serializer
    # expect an 'email' key in the request. We want it to accept 'username' key (standard for SimpleJWT)
    # but treat the value as an email.

    def validate(self, attrs):
        # The frontend sends 'username' and 'password'
        # We treat the 'username' value as an email
        email = attrs.get('username')
        password = attrs.get('password')

        if email and password:
            # Find user by email
            user = User.objects.filter(email=email).first()
            if user:
                # Replace the email with the actual username so authentication works
                attrs['username'] = user.username
            else:
                # If user not found, let it fail naturally (it will try to auth with email as username and fail)
                pass
                
        return super().validate(attrs)

