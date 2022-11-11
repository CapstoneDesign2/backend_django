from rest_framework import serializers
from .models import Cafe, Review, Signuptest


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('place_name',)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','reviewer_name','content')
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signuptest
        fields = ('id','name')

class CafeLocationSerializer(serializers.ModelSerializer):
    
    """
    my_field = serializers.SerializerMethodField()
    
    def get_my_field(self, cafe_instance):
        return cafe_instance.x + cafe_instance.y
    """
    class Meta:
        model = Cafe
        fields = ('id','place_name','x','y')     
        


    