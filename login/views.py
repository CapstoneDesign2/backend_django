from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from quiz.models import User
from quiz.serializers import UserSerializer 
from rest_framework import status
from django.http.response import HttpResponse
from django.http import JsonResponse
from MyJsonResponse import jres
# Create your views here.

#sumry: 이메일 받아서 중복여부를 검사한다.
#param: email
#usage: /login/sign_up/double_check?email=
@api_view(['GET'])
def doubleCheckAPI(request):
    curEmail = str(request.GET['email'])
    check = User.objects.filter(email=curEmail)
    return jres(False) if check.count() > 0 else jres(True)

    if check.count() > 0:
        return jres(False)#JsonResponse({'message':'Fail'},status=200)#HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        return jres(True)#JsonResponse({'message':'Success'},status=200)#HttpResponse(status=200,)

#sumry: 이메일, 암호 받아서 db에 저장
#param: data
#usage: /login/sign_up/register
@api_view(['POST'])
def registerAPI(request):
    newUser = User.objects.create(email=request.data['email'],password=request.data['password'])
    return jres(True,UserSerializer(newUser).data) #JsonResponse(UserSerializer(newUser).data,status=200)

#sumry: 이메일, 암호 받아서 로그인 시도.
#param: email, password
#usage: /login/login?email&password
@api_view(['GET'])
def loginAPI(request):
    curEmail = str(request.GET['email'])
    curPassword = str(request.GET['password'])
    userInfo = User.objects.filter(email=curEmail,password=curPassword)
    return jres(True) if userInfo.count() > 0 else jres(False)

    if userInfo.count() >0:
        return jres(False) #JsonResponse({'message':'Fail'},status=200)#Response(status=200)
    else:
        return jres(True)#JsonResponse({'message':'Success'},status=200)#Response(status=status.HTTP_400_BAD_REQUEST)