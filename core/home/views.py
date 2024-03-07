from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeopleSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        courses = {
        'courses_name': 'Python',
        'learn' : ['flask', 'Django', 'Tornado', 'fastapi'],
        'course_provider': 'Scaler',
        'method': 'GET'
        }
    else:
       data = request.data
       print(data)
       courses = {
        'courses_name': 'Python',
        'learn' : ['flask', 'Django', 'Tornado', 'fastapi'],
        'course_provider': 'Scaler'
    }
       
    return Response(courses)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'data deleted'})