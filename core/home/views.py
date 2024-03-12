from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from rest_framework.decorators import action

class LoginAPI(APIView):
    def post(self, request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_404_BAD_REQUEST)
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data["password"])
        if not user:
            return Response({
                'status': False,
                'message': 'invalid credentials'
            }, status.HTTP_404_BAD_REQUEST)
            
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status': True, 'message': 'user login', 'token': str(token) }, status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data 
        serializer = RegisterSerializer(data = data)
        
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_404_BAD_REQUEST)
            
        serializer.save()
        
        return Response({'status': True, 'message': 'user created' }, status.HTTP_201_CREATED)
        

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

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message' : 'success'})
        
    return Response(serializer.errors)

class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            print(request.user)  #to get which user is authenticated
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
        
            paginator = Paginator(objs, page_size)
            print(paginator.page(page))
            serializer = PeopleSerializer(paginator.page(page), many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                'status': False,
                'message' : 'invalid page'
            })
        # return Response({'message': 'This is a get request'})
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'data deleted'})


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


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post']
    
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
            
        serializer = PeopleSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def send_mail_to_person(self, request, pk):
        print(pk)
        obj = Person.objects.get(pk=pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'status':True,
            'message': 'email sent successfully',
            'data' : serializer.data
        })