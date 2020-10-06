from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from .models import Poll, Choice, Vote
# Create your views here.

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset
    serializer_class = ChoiceSerializer

class CreateVote(APIView):
    serializer_class = VoteSerializer
    
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    """
    Giving exemption to UserCreate view for authentication by overriding the global setting
    authentication_classes = () and permission_classes = () will do the job
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer