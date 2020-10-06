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
    
class UserSerializer(serializers.ModelSerializer):
    """
    Overriden the modelSerializer method's create to save the User
    instances.
    We ensure that we set the password correctly using user.set_password
    rather than setting the raw password as the hash. We also don't want to get back 
    the password in response which we ensure using the extra_kwargs
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True}}
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user