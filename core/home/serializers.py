from rest_framework import serializers
from .models import Person, Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name', 'id']

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    class Meta:
        model = Person
        # fields = ['age']
        fields = '__all__'
        # exclude = ['name']  #to exclude a particular field
        # depth = 1
        
    def validate(self, data):
        special_characters = '[^\\\\/`~!@#$%^&*:*?\"<>|.]*'
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special characters')
        
        
        
        if data['age'] < 18:
            raise serializers.ValidationError('age should be greater than 18')
        
        return data