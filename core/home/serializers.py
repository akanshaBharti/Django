from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is taken')
    
    
        if data['email']:
            if User.objects.filter(username = data['email']).exists():
                raise serializers.ValidationError('email is taken')
            
        return data
    
    def create(self, validated_data):
        user = user.objects.create(username = validated_data["username"], email = validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data
        print(validated_data)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name', 'id']

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        # fields = ['age']
        fields = '__all__'
        # exclude = ['name']  #to exclude a particular field
        # depth = 1
        
    def get_color_info(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {'color_name': color_obj.color_name, 'hex_code' : '#000'}
        # return "India"
        
    def validate(self, data):
        special_characters = '[^\\\\/`~!@#$%^&*:*?\"<>|.]*'
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special characters')
        
        
        
        # if data.get('age') and data['age'] < 18:
        #     raise serializers.ValidationError('age should be greater than 18')
        
        return data