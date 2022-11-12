from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cafe, Review, Signuptest
from .serializers import CafeSerializer, ReviewSerializer, TestSerializer, CafeLocationSerializer 
from rest_framework import status
import random
# Create your views here.
 

# sumry: 테스트용 api.
# param:
# usage: /quiz/hello
@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")

# sumry: 카페를 count개 만큼 불러온다.
# param: count
# usage: /quiz/cafe?count=3
@api_view(['GET'])
def cafeAPI(request):
    numberOfCafe = int(request.GET['count'])
    cafes = Cafe.objects.all()[0:numberOfCafe]
    serializer = CafeSerializer(cafes,many=True)
    return Response(serializer.data)

# sumry: id(카페id)에 맞는 리뷰를 count개 만큼 불러온다.
# param: id, count 
# usage: /quiz/review?id=1&count=3
@api_view(['GET'])
def reviewAPI(request):
    cafeId = int(request.GET['id'])
    numberOfReview = int(request.GET['count'])
    reviews = Review.objects.filter(id=cafeId)[0:numberOfReview]
    serializer = ReviewSerializer(reviews,many=True)
    return Response(serializer.data)

# sumry: user 의 현재 x , y 좌표를 가져온다.
# param: x, y
# usage: /quiz/location?x=&y=
@api_view(['GET'])
def cafeLocationAPI(request):
   
    curX = float(request.GET['x'])
    curY = float(request.GET['y'])
    
    # 가능 cafeLocationlist = Cafe.objects.raw('SELECT * FROM Cafe WHERE (x + y) > (%s - %s)',([curX],[curY]))
    # 가능 cafeLocationlist = Cafe.objects.raw('SELECT * FROM Cafe WHERE (x + y) > 164.492')
    
    CafeLocationlist = Cafe.objects.raw('SELECT id, ST_Distance_Sphere(Point(x,y), Point(%s,%s)) as Distance FROM Cafe WHERE ST_Distance_Sphere(Point(x,y), Point(%s,%s)) <= 50 ORDER BY Distance',([curX],[curY],[curX],[curY]) )
    
    serializer = CafeLocationSerializer(CafeLocationlist,many=True)
    return Response(serializer.data)


#성원 의미없는 주석
#성원 의미없는 주석2

'''
@api_view(['GET'])
def randomQuiz(request,id):
    totalQuizs = Quiz.objects.all()
    randomQuizs = random.sample(list(totalQuizs),id)
    serializer = QuizSerializer(randomQuizs,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cafeAPI(request):
    return Response("cafeishorse")

@api_view(['GET'])
def gradeCafe(request):
    cafeList = Cafe.objects.all().order_by('-grade')
    serializer = CafeSerializer(cafeList,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review(request):
    reviewList = Review.objects.all()
    serializer = ReviewSerializer(reviewList, many=true)
    return Response(serializer.data)
'''