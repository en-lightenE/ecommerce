from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        exclude = ("last_login",)
        
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Passowrd2 don't match")
        return attrs
    
    
    def create(self, validate_data):
        del validate_data['password2']
        return User.objects.create(**validate_data)
    
    def get_first_name(self, obj):
        return obj.fname

    def get_last_name(self, obj):
        return obj.lame

    def get_full_name(self, obj):
        first_name = obj.user.fname
        last_name = obj.user.lname
        return f"{first_name} {last_name}"

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "date_of_birth", "email", "fname", "lname", "password"]