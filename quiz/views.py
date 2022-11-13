from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Bookmark, Cafe, Review, User
from .serializers import BookmarkSerializer, CafeSerializer, ReviewSerializer, CafeLocationSerializer, UserSerializer
from rest_framework import status
from django.http import JsonResponse
from MyJsonResponse import jres
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
    
    CafeLocationlist = Cafe.objects.raw('SELECT id, ST_Distance_Sphere(Point(x,y), Point(%s,%s)) as Distance FROM Cafe WHERE ST_Distance_Sphere(Point(x,y), Point(%s,%s)) <= 50 ORDER BY Distance',([curX],[curY],[curX],[curY]) )
    
    serializer = CafeLocationSerializer(CafeLocationlist,many=True)
    return jres(True, serializer.data)#Response(serializer.data)

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