from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Welcome user:"+request.POST["custom_course_id"]+"to the course with id: "+ request.POST["custom_user_id"])

