from polls.models import Question, Choice, User
from rest_framework import viewsets, permissions
from .serializers import QuestionSerializer, ChoiceSerializer, UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    # queryset = Question.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        qid = self.request.query_params.get('qid', None)
        if qid is not None:
            queryset = queryset.filter(pk=qid)
        return queryset

class ChoiceViewSet(viewsets.ModelViewSet):
    # queryset = Choice.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.all()
        qid = self.request.query_params.get('qid', None)
        get_highest = self.request.query_params.get('qid', None)

        if qid is not None:
            queryset = queryset.filter(question=qid)
        # if get_highest is not None:
        #     queryset = Choice.objects.raw('SELECT * FROM polls_choice WHERE question_id = {} Group by choice_text '.format(qid))
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
