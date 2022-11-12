from rest_framework import serializers
from .models import Cafe, Review


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('id','place_name','phone','x','y')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','reviewer_name','content')

class CafeLocationSerializer(serializers.ModelSerializer):
    
    """
    my_field = serializers.SerializerMethodField()
    
    def get_my_field(self, cafe_instance):
        return cafe_instance.x + cafe_instance.y
    """
    class Meta:
        model = Cafe
        fields = ('id','place_name','x','y')     
        


    