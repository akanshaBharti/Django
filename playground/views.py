from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# view function takes a request and response accordingly

def calculate():
    x=1
    y=2
    return x

def say_hello(request): 
    # pull daa from db, transform data, send email
    # return HttpResponse('Hello World')
    x =  calculate()
    return render(request, 'hello.html', {'name': 'Akansha'})
    
