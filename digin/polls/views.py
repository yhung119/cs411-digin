from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse

from .models import Choice, Question, Vote, Poll_members, Archive_question, Place
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone
from django.db import connection
from django.db.models.expressions import RawSQL

from django.utils.timesince import timesince
import collections
import random
from .review_views import generate_wordcloud
from .googleUtil import get_restaurant_attr
import json


class HomePageView(TemplateView):
    template_name = 'home.html'

class IndexView(generic.ListView):
    
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    # @login_required
    def get_queryset(self):
        # print(self.request.user)
        """Return the last five published questions."""
        if self.request.user.is_anonymous:
            return None
        user_polls = Poll_members.objects.filter(member=self.request.user)
        
        question_ids = [poll.question.id for poll in user_polls]
        # print(question_ids)
        return Question.objects.filter(pk__in=question_ids)#Question.objects.raw("SELECT * FROM polls_question ORDER BY pub_date DESC")

def get_winning_choice(question_id):
    '''
    returns the winning chocie of the given question
    saves the winning choice to arcieve question table
    
    TODO:
        handle the case when there is no vote in that question
    '''
    # get the votes
    votes = Vote.objects.filter(question_id=question_id)

    # calcuate the choices with highest vote
    choices = collections.defaultdict(int)
    max_vote = 0
    for vote in votes:
        choices[vote.choice_id] += 1
        if (max_vote < choices[vote.choice_id]):
            max_vote = choices[vote.choice_id]
    
    winning_choices = []

    for key, val in choices.items():
        if (val == max_vote):
            winning_choices.append(key)
    question = Question.objects.get(id=question_id)
    winning_choice = winning_choices[random.randint(0,len(winning_choices)-1)]
    arch_question = Archive_question(question=question, best_choice=Choice.objects.get(id=winning_choice))
    arch_question.save()
    return Choice.objects.get(id=winning_choice)

class DetailView(generic.DetailView):
    '''
    view that shows the choices of each question

    '''
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["choices"] = Choice.objects.raw("SELECT * FROM polls_choice WHERE question_id = %s",[context["question"].id])
        
        
        if context["question"].is_active is False:
            context["winner"] = Choice.objects.get(id=Archive_question.objects.get(question=context["question"]).best_choice.id)
            return context

        if context["question"].deadline < timezone.now():
            context["question"].is_active=False
            winner = get_winning_choice(context["question"].id)
            context["winner"] = winner
            context["question"].save()
        
        # print(context["question"].deadline - timezone.now() > 0)
        ## the context is a list of the tasks of the Project##
        ##THIS IS THE ERROR##
        
        return context



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class EditView(generic.DetailView):
    model = Question
    template_name = 'polls/edit.html'

class AddUserView(generic.DetailView):
    model = Question
    template_name = 'polls/adduser.html'



def vote(request, question_id):
    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    choices_query = Choice.objects.raw("SELECT * FROM polls_choice WHERE question_id=%s", [question_id])
    choices = []
    for choice in choices_query:
        choices.append(choice)
    
    try:        
        selected_choice = Choice.objects.raw("SELECT * FROM polls_choice WHERE id=%s",[request.POST['choice']])
    except (KeyError, Choice.DoesNotExist):
        
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'choices': choices,
            'error_message': "You didn't select a choice.",
        })
    else:
        if request.POST.get("Delete"):
            choicedel = question.choice_set.get(pk=request.POST['choice'])
            choicedel.delete()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
        else:
            try:
                # Vote.objects.get(question=question, owner=request.user, choice=selected_choice[0])
                vote = Vote.objects.raw("SELECT * FROM polls_vote WHERE question_id=%s AND owner_id=%s AND choice_id=%s", [question.id, request.user.id, selected_choice[0].id])[0]
                # print([question.id, request.user.id, selected_choice[0].id])
            except (IndexError, Vote.DoesNotExist):
                cursor = connection.cursor()
                cursor.execute("UPDATE polls_choice SET votes = votes+1 WHERE id=%s", [request.POST['choice']])
                cursor.execute("INSERT INTO polls_vote (question_id, owner_id, choice_id) VALUES (%s, %s, %s) ", [question.id, request.user.id, selected_choice[0].id])
                # v=Vote(question=question,owner=request.user,choice=selected_choice[0])
                # v.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
            else:
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'choices': choices,
                    'error_message': "You have already voted.",
                })

def addChoice(request, question_id):

    current_user=request.user
    inp_value = request.POST.get('choice')
    
    place_id=request.POST.get('placeId')
    print("place_id:{}".format(place_id))
    if place_id != "":
        attrs = get_restaurant_attr(place_id)
    else:
        attrs = [inp_value,"unknown address","unknown phone", 2, 2, "", [""], 0, 0, "www.google.com"]
    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    generate_wordcloud(place_id, attrs[6])
    print(attrs)
    attrs[6] = json.dumps(attrs[6])
    cursor = connection.cursor()

    place = Place.objects.raw("SELECT * FROM polls_place WHERE place_id=%s", [attrs[5]])
    # print(place)
    # print(type(place))
    if (len(list(place))==0):
        cursor.execute("INSERT INTO polls_place"
                    "(name, address, phone, rating, price_level, place_id, reviews, latitude, longitude, website)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    attrs
                    )
    choice = Choice.objects.raw("SELECT * FROM polls_choice WHERE place_id=%s AND question_id=%s", [attrs[5], question_id])
    if (len(list(choice)) == 0):
        cursor.execute("INSERT INTO polls_choice"
                    "(question_id, owner_id, place_id, name, votes)"
                    "VALUES (%s, %s, %s, %s, 0)",
                    [question_id, current_user.id, attrs[5], attrs[0]]
                    )


    # question.choice_set.create(choice_text=inp_value,votes=0,owner=request.user)
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    

def addQuestion(request):
    inp_value = request.POST.get('question')
    deadline = request.POST.get('deadline')
    q = Question(question_text=inp_value,pub_date=timezone.now(),owner=request.user, deadline=deadline, is_active=True)
    q.save()
    poll_mem = Poll_members(member=request.user, question=q)
    poll_mem.save()
    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO polls_question"
    #                "(question_text, pub_date, owner_id, deadline)"
    #                "VALUES (%s, NOW(), %s, %s)",
    #                (inp_value, request.user.id)
    #                )
    return HttpResponseRedirect(reverse('polls:home'))



   
def delQuestion(request, question_id):
    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM polls_question WHERE id=%s AND owner_id=%s",
                    (question_id, request.user.id))
    return HttpResponseRedirect(reverse('polls:index'))


def editQuestion(request,question_id):
    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    inp_value=request.POST.get('choice')
    cursor = connection.cursor()
    cursor.execute("UPDATE polls_question SET question_text = %s WHERE id=%s AND owner_id=%s", [inp_value, question_id, request.user.id])
    return HttpResponseRedirect(reverse('polls:index'))



def addUser(request, question_id):
    """
    TODO:
        make sure duplicate is not added. Either fixed it on the database level or 
        implement on API.

    """
    user = request.user
    inp_value = request.POST.get('name')
    

    member_id = CustomUser.objects.filter(name=inp_value)
    question = Question.objects.get(id=question_id)

    # checking that onwer is not adding himself or user doesn't exist
    if (len(member_id) != 1 or Poll_members.objects.filter(member=member_id[0], question=question).exists()):
        return HttpResponseRedirect(reverse('polls:index'))
    
    new_member = Poll_members(member=member_id[0], question=question)
    
    new_member.save()
    
    return HttpResponseRedirect(reverse('polls:index'))

def get_data(request,*args,**kwargs):
    print("hello")
    cur=connection.cursor();
    cur.execute("SELECT c.name, COUNT(*) FROM polls_vote v, polls_choice c WHERE c.id=v.choice_id GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 5")
    convert=cur.fetchall()
    data=dict((x, y) for x, y in convert)
    print(data)
    return JsonResponse(data)

