from rest_framework import serializers
from .models import Cafe, Review


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = (
            'id','place_name','phone','x','y',
             'road_address_name','main_photo','star_mean'
                )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id','store','username','contents',
            'point','photocnt','likecnt',
            'usercommentcount','usercommentaveragescore',
            'date','kakaomapuserid'
        )

class CafeLocationSerializer(serializers.ModelSerializer):
    
    """
    my_field = serializers.SerializerMethodField()
    
    def get_my_field(self, cafe_instance):
        return cafe_instance.x + cafe_instance.y
    """
    class Meta:
        model = Cafe
        fields = ('id','place_name','x','y')     
        


    