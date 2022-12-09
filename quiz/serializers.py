from rest_framework import serializers
from .models import Bookmark, Cafe, Review, User


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = (
            'id','place_name','phone','x','y',
             'road_address_name','main_photo','star_mean','bookmark_cnt','comment_count'
             
                )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id','store','username','contents',
            'point','photocnt','likecnt',
            'usercommentcount','usercommentaveragescore',
            'date','kakaomapuserid','photolist'
        )

class CafeLocationSerializer(serializers.ModelSerializer):
    
    """
    my_field = serializers.SerializerMethodField()
    
    def get_my_field(self, cafe_instance):
        return cafe_instance.x + cafe_instance.y
    """
    class Meta:
        model = Cafe
        fields = ('id','place_name','x','y', 'road_address_name','main_photo','star_mean','bookmark_cnt','comment_count','tasty','clean','effective','vibe','kind')     
        

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = (
            'id','user_id'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')