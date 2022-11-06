from rest_framework import serializers
from .models import Cafe, Review, Signuptest


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('id','place_name','phone','x','y')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','reviewer_name','content')
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signuptest
        fields = ('id','name')
    
    