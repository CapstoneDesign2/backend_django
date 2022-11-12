from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer 
from rest_framework import status
from django.http.response import HttpResponse
# Create your views here.

#sumry: 이메일 받아서 중복여부를 검사한다.
#param: email
#usage: /login/sign_up/double_check?email=
@api_view(['GET'])
def doubleCheckAPI(request):
    curEmail = str(request.GET['email'])

    #유저 정보 중 겹치는 이메일이 있는지 검사한다.
    check = User.objects.filter(email=curEmail)

    if check.count() >0:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse(status=200)

#sumry: 이메일, 암호 받아서 db에 저장
#param: data
#usage: /login/sign_up/register?email=&password=
@api_view(['POST'])
def registerAPI(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        #저장
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

#sumry: 이메일, 암호 받아서 로그인 시도.
#param: email, password
#usage: /login/login?email&password
@api_view(['GET'])
def loginAPI(request):
    curEmail = str(request.GET['email'])
    curPassword = str(request.GET['password'])

    userInfo = User.objects.filter(email=curEmail,password=curPassword)
    if userInfo.count() >0:
        return Response(status=200)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
