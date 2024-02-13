from rest_framework import serializers
from .models import Person

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'   # to add all fields use __all__, to exclude some fields use exclude = ['fieldname', 'fieldname']