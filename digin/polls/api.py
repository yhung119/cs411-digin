from polls.models import Question, Choice, User
from rest_framework import status, viewsets, permissions
from .serializers import QuestionSerializer, ChoiceSerializer, UserSerializer
from django.db import connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import connection

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
        get_highest = self.request.query_params.get('highest', None)

        if qid is not None:
            queryset = Choice.objects.raw('SELECT * FROM polls_choice WHERE question_id = %s', [qid])
            if get_highest is not None:
                query = """SELECT * 
                            FROM polls_choice pout,
                                (SELECT choice_text, SUM(votes) 
                                from polls_choice
                                where question_id = %s
                                group by choice_text 
                                having SUM(votes) = (
                                    select MAX(vs)  
                                    from (select SUM(votes)  vs 
                                        from polls_choice
                                        where question_id = %s
                                        group by choice_text) tmp)
                                ) v_sum
                            WHERE pout.question_id = %s AND pout.choice_text = v_sum.choice_text
                        """
                queryset = Choice.objects.raw(query, [qid, qid, qid])
        elif get_highest is not None:
            query = """SELECT * 
                        FROM polls_choice pout,
                            (SELECT choice_text, SUM(votes) 
                            from polls_choice
                            group by choice_text 
                            having SUM(votes) = (
                                select MAX(vs)  
                                from (select SUM(votes)  vs 
                                    from polls_choice
                                    group by choice_text) tmp)
                            ) v_sum
                        WHERE pout.choice_text = v_sum.choice_text
                    """
            queryset = Choice.objects.raw(query)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    @action(detail=True, methods=['put'])
    def custom_put(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("UPDATE polls_user SET location = %s, email = %s, name = %s WHERE id = %s", 
                [serializer.data['location'], serializer.data['email'], serializer.data['name'], pk])
            return Response({'status': 'update set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def custom_delete(self, request, pk=None):
        cursor = connection.cursor()
        cursor.execute("SELECT * from polls_user WHERE id = %s", [pk])
        if cursor.fetchone() == None:
            raise ValidationError('no object to delete')
        else:
            cursor.execute("DELETE from polls_user WHERE id = %s", [pk])
            return Response({'status': 'delete set'})
