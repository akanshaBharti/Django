from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from homw.serializers import PeopleSerializer


@api_view(['GET', 'POST'])
def index(request):
    # courses = {
    #     'course_name' : 'Python',
    #     'learn' : ['flask', 'Django', 'Tornado', 'FastApi'],
    #     'course_provider' : 'Scaler'
    # }
    if request.method == 'GET':
        json_response = {
            'name': 'Scaler',
            'courses' : ['C++', 'Python'],
            'method' : 'GET'
        }
    else: 
        data = request.data
        print(data)
        json_response = {
            'name': 'Scaler',
            'courses' : ['C++', 'Python'],
            'method' : 'POST'
        }
    return Response(json_response)
        # print(request.GET.get('search'))
        # print('You HIT a get method')
        # return Response(courses)
    # elif request.method == 'POST':
    #     data = request.data
    #     print(data)
    #     print('you hit a POST method')
    #     return Response(courses)
    # elif request.method == 'PUT':
    #     print('you hit a PUT method')
    #     return Response(courses)
    
@api_view(['GET', 'POST'])
def person(request):
    if request.GET:
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    else:
        data = request.data
        serializer = PeopleSerializer(data = data)
    