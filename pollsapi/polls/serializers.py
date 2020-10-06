from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Poll, Choice, Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Vote
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(Many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'
    
class 