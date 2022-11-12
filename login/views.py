from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer 
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def doubleCheckAPI(request):
    curEmail = str(request.GET['email'])

    #유저 정보가 이미 있는지 검사한다.
    check = User.objects.filter(email=curEmail)
    if check.count>0:
        return Response()
    else:
        return Response()

@api_view(['POST'])
def registerAPI(request):
    return Response()


@api_view(['GET'])
def loginAPI(request):
    return Response()
