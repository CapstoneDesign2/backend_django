from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Bookmark, Cafe, Review, User
from .serializers import BookmarkSerializer, CafeSerializer, ReviewSerializer, CafeLocationSerializer, UserSerializer
from rest_framework import status
from django.http import JsonResponse
from MyJsonResponse import jres
from haversine import haversine
import random
import pandas as pd
import numpy as np
from numpy import dot 
from numpy.linalg import norm
import json

# Create your views here.

# sumry: 테스트용 api.
# param:
# usage: /quiz/hello
@api_view(['GET'])
def helloAPI(request):
    return Response("hello world! Test clear")

# sumry: 카페를 count개 만큼 불러온다.
# param: count
# usage: /quiz/cafe?count=3
@api_view(['GET'])
def cafeAPI(request):
    
    numberOfCafe = int(request.GET['count'])
    cafes = Cafe.objects.all()[0:numberOfCafe]
    serializer = CafeSerializer(cafes,many=True)
    print(type(serializer))
    return jres(True, serializer.data) #Response(serializer.data)
   
# sumry: id(카페id)에 맞는 리뷰를 count개 만큼 불러온다.
# param: id, count 
# usage: /quiz/review?id=1&count=3
@api_view(['GET'])
def reviewAPI(request):
    cafeId = int(request.GET['id'])
    numberOfReview = int(request.GET['count'])
    reviews = Review.objects.filter(store=cafeId)[0:numberOfReview]
    serializer = ReviewSerializer(reviews,many=True)
    return jres(True, serializer.data)#Response(serializer.data)

# sumry: user 의 현재 x , y 좌표를 가져온다.
# param: x, y
# usage: /quiz/location?x=&y=
# 의미없는 주석
# 의미없는 추석
@api_view(['GET'])
def cafeLocationAPI(request):
   
    curX = float(request.GET['x'])
    curY = float(request.GET['y'])
    
    # 가능 cafeLocationlist = Cafe.objects.raw('SELECT * FROM Cafe WHERE (x + y) > (%s - %s)',([curX],[curY]))
    # 가능 cafeLocationlist = Cafe.objects.raw('SELECT * FROM Cafe WHERE (x + y) > 164.492')
    
    CafeLocationlist = Cafe.objects.raw('SELECT id FROM Cafe WHERE ST_Distance_Sphere(Point(x,y), Point(%s,%s)) <= 500',([curX],[curY]))
    cafeList = CafeLocationSerializer(CafeLocationlist,many=True).data

    for cafe in cafeList:
        cafe['distance'] = get_distance(curX,curY,cafe)
 
    return jres(True, cafeList)#Response(serializer.data)

#sumry: 찜 버튼을 클릭했을 때 카페의 찜 카운트를 +1하고 유저의 찜 목록에 추가한다.
#param: email, id
#usage: /quiz/cafe/bookmark/enable?email=&id=
@api_view(['PUT'])
def bookmarkEnableAPI(request):
    curEmail = str(request.GET['email'])
    curCafeId = int(request.GET['id'])
    #이메일 이용해서 유저 데이터 찾음.
    curUser = User.objects.get(email=curEmail)
    
    IsBookmarkExist = Bookmark.objects.filter(id=curCafeId,user_id=curUser.user_id)
    if IsBookmarkExist.count() > 0:
        return jres(False)  #JsonResponse({'message':'Fail'},status=200)

    curBookmark = Bookmark.objects.create(user_id = curUser.user_id,id=curCafeId)

    #만들기 예제: 
    # curBookmark = Bookmark(user_id=0, id = 1)
    # curBookmark.save(force_insert=True)
    # 또는
    # curBookmark = Bookmark.objects.create(user_id=0,id=1)

    #카페 데이터 찾아서 북마크 +1 후 저장.
    curCafe = Cafe.objects.get(id=curCafeId)
    curCafe.bookmark_cnt += 1
    curCafe.save()
    cafeSerializer = CafeSerializer(curCafe)
    return jres(True,cafeSerializer.data) #JsonResponse({'message':'Success'},data = cafeSerializer.data, status=200)#Response(cafeSerializer.data, status=200)

#sumry: 찜 버튼을 클릭했을 때 카페의 찜 카운트를 -1하고 유저의 찜 목록에서 제거한다.
#param: email, id
#usage: /quiz/cafe/bookmark/disable?email=&id=
@api_view(['DELETE'])
def bookmarkDisableAPI(request):
    curEmail = str(request.GET['email'])
    curCafeId = int(request.GET['id'])
    #이메일 이용해서 유저 데이터 찾음.
    curUser = User.objects.get(email=curEmail)

    isNotExistBookmark = Bookmark.objects.filter(user_id=curUser.user_id, id=curCafeId)

    if isNotExistBookmark.count() == 0:
        return jres(False) #JsonResponse({'message':'Fail'},status=200)

    Bookmark.objects.get(user_id=curUser.user_id, id=curCafeId).delete()

    #카페 데이터 찾아서 북마크 -1 후 저장.
    curCafe = Cafe.objects.get(id=curCafeId)
    curCafe.bookmark_cnt -= 1
    curCafe.save()
    cafeSerializer = CafeSerializer(curCafe)
    return jres(True,cafeSerializer.data) #JsonResponse({'message':'success'},data = cafeSerializer.data, status=200)#Response(cafeSerializer.data, status=200)

#sumry: 유저가 해당 카페를 찜했는지 여부를 리턴한다.
#param: email, id
#usage: /quiz/cafe/bookmark/is?email=&id=
@api_view(['GET'])
def isBookmarkAPI(request):
    curEmail = str(request.GET['email'])
    curCafeId = int(request.GET['id'])
     #이메일 이용해서 유저 데이터 찾음.
    curUser = User.objects.get(email=curEmail)
    curBookmark = Bookmark.objects.filter(user_id=curUser.user_id,id=curCafeId)

    if curBookmark.count() >0:
        return jres(True) #JsonResponse({'message':'Success'},status=200)#Response(status=200)
    else:
        return jres(False) #Response(status=status.HTTP_400_BAD_REQUEST)

#sumry: 카페를 찜순으로 정렬해서 리턴한다.
#param: count
#usage: /quiz/cafe/bookmark?count=
@api_view(['GET'])
def orderByBookmarkAPI(request):
    numberOfCafe = int(request.GET['count'])
    cafes = Cafe.objects.all().order_by('-bookmark_cnt')[0:numberOfCafe]
    serializer = CafeSerializer(cafes,many=True)
    return jres(True,serializer.data) #Response(serializer.data), 반드시 복구

#sumry: 유저가 찜한 카페를 리턴한다.
#param: email
#usage: /quiz/cafe/bookmark/list?email=
@api_view(['GET'])
def bookmarkListAPI(request):
    curEmail = str(request.GET['email'])
    curUser = User.objects.get(email=curEmail)
    bookmarkedCafeList = Bookmark.objects.filter(user_id=curUser.user_id).values_list('id',flat=True)
    cafes = Cafe.objects.filter(id__in=bookmarkedCafeList)
    serializer = CafeSerializer(cafes,many=True)
    return jres(True, serializer.data) #Response(serializer.data)

#sumry: 추천 순으로 정렬한다.
#param: keyword1~keyword5, location
#usage: /quiz/cafe/recommend?keyword1=&...keyword3=&x=&y=&loc=
@api_view(['GET'])
def recommendAPI(request):

    curX = float(request.GET['x'])
    curY = float(request.GET['y'])
    rLoc = float(request.GET['loc'])

    keywordList = []

    # keyword1 ~ keyword3
    for i in range(1,4):
        try:
            curKeyword = (request.GET['keyword'+str(i)])
            keywordList.append(curKeyword)
        
        except:
            pass
    
    #1. 일정 거리 안에 있는 카페를 DB에서 가져온다.
    #cafeModelList = Cafe.objects.raw('SELECT id, ST_Distance_Sphere(Point(x,y), Point(%s,%s)) as Distance FROM Cafe WHERE ST_Distance_Sphere(Point(x,y), Point(%s,%s)) <= %s ORDER BY Distance',([curX],[curY],[curX],[curY],[rLoc]) )
    #CafeLocationlist = Cafe.objects.raw('SELECT id FROM Cafe WHERE ST_Distance_Sphere(Point(x,y), Point(%s,%s)) <= %s',([curX],[curY],[rLoc]))
    cafeModelList = Cafe.objects.all()
    cafeList = CafeLocationSerializer(cafeModelList,many=True).data

    #2. 각 카페에 대해서 유사도를 계산한다(핵심).
    for cafe in cafeList:
        cafe['distance'] = get_distance(curX,curY,cafe)
    
    
    
    #코드
        
    #데이터 전처리
    
    #1_1. 데이터 df화
    df_cafe = pd.DataFrame(cafeList)
    
    
    #1_1. 임시 csv파일
    #txt_path = "cafe.csv"
    #df = pd.read_csv(txt_path, sep='|')
    
    #1_2. 필요한 Data column 추출 
    df_t = df_cafe[['tasty','clean','effective','kind','vibe']]
    df_t =df_t.replace(np.nan,0.0)
    
    
    
    #가중치 설정 
    #받은 키워드를 순서대로 가중치 1, 0.8, 0.6으로 부여 
    df_t_column = df_t.columns.values.tolist()
    #형식을 맞춤
    
    weight_t = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
    
    k = 10
    for i in range(0, 3):
        for j in range(0, 5):
            if(keywordList[i] == df_t_column[j]): 
                weight_t[j] *= k
                k -= 2
                
    #유사도 구하기
    
    #1.데이터 평준화 과정     
    max = df_t.max().to_numpy()     
    max_sum = max.sum()
    max_sum_f = max_sum / max   
    
    #2.평준화된 데이터에 가중치를 곱함
    r_max = max_sum_f * weight_t
    
    #3.최적카페 
    standard_cafe = np.array([50, 50, 50, 50, 50]) 

    
    #4.유클리디언 유사도 계산 / 코사인 유사도 쓰면 안됨 / 맨헤튼 
    test = []
    count = len(df_t.index)
    #print(count)
    
    for i in range(0,count):
        temp_np = (df_t.iloc[i].to_numpy() / standard_cafe) * r_max 
        #temp = euc_sim(standard_cafe,temp_np)
        temp = manhattan_distance(standard_cafe,temp_np)
        test.append(temp)
        df_t.iloc[i] = temp_np * standard_cafe / r_max

    #5.유사도로 정렬
    df_t['euc'] = test       
    df_t = df_t.sort_values(by=['euc'])
    
    print(df_t)
    
    #6.결과값을 기준으로 카페를 다시 재정렬하고 json파일로 변환    
    df_t_index = (df_t.index).to_numpy()   
    df_result = df_cafe.reindex(df_t_index)
    df_result = df_result.replace(np.nan,0.0)
    
    print(df_result)                  
    #result = (df_result.reset_index().to_json(orient='records'))
    #코드
    
    result = df_result.to_dict(orient='records')
    #result = df_result.reset_index().to_json(orient='records')
    #print(type(result))
    
    #result1 = json.loads(df_result)
    #result2 = json.dump(result1)
    
    #print(type(result2))
    
    #임시 결과값
    
    return jres(True, result)
    
    #return jres(True, cafeList)

def get_distance(x, y, cafe):
    
    cafeX = float(cafe['y'])
    cafeY = float(cafe['x'])

    cafePoint = (cafeX, cafeY)
    userPoint = (y,x)

    return haversine(cafePoint, userPoint, unit = 'm')

def cos_sim(A, B, C):
    return dot((A*C), (B*C))/(norm(A) * norm(B))

def euc_sim(A, B):
   return np.sqrt(np.sum((A-B)**2))

def manhattan_distance(x,y): 
    return sum(abs(a-b) for a,b in zip(x,y))
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