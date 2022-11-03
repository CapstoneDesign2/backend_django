from rest_framework import serializers
from .models import Cafe, Review


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('id','cafe_name')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','reviewer_name','content')