from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Quiz, Cafe
from .serializers import CafeSerializer, QuizSerializer
import random
# Create your views here.
 


@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")

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

