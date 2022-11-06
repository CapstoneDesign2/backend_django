from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cafe, Review, Signuptest
from .serializers import CafeSerializer, ReviewSerializer, TestSerializer
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

# signup Test code
@api_view(['POST'])
def signupTestAPI(request):
    reqData = request.data
    serializer = TestSerializer(data = reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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