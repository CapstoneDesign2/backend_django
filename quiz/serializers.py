from rest_framework import serializers
from .models import Quiz, Cafe

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('title','body','answer')
        
class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('name','charactor','grade','Location')