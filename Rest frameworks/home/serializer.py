from rest_framework import serializers
from .models import Person

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

# depth gives all the data, whereas when serializer class is used it gives particular data
class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer(many=True)
    class Meta:
        model = Person 
        fields = '__all__'   # to add all fields use __all__, to exclude some fields use exclude = ['fieldname', 'fieldname']
        # depth = 1
        
    def validate(self, data):
        special_characters = "!@#$%^&*)(':;-+?_=,<>/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special chars')
        if data['age'] < 18:
            raise serializers.ValidationError('age should be greater than 18')
        return data