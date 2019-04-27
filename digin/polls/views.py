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
import subprocess


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
        user_polls = Poll_members.objects.raw("SELECT * FROM polls_poll_members WHERE member_id=%s", [self.request.user.id])
        #filter(member=self.request.user)
        
        question_ids = [poll.question.id for poll in user_polls]
        question_ids = tuple(question_ids)
        print(len(question_ids))
        if (len(question_ids) == 0):
            return None
        query = Question.objects.raw("SELECT * FROM polls_question WHERE id IN %s", [question_ids])#Question.objects.filter(pk__in=question_ids)#Question.objects.raw("SELECT * FROM polls_question ORDER BY pub_date DESC")
        return query
        
def get_winning_choice(question_id):
    '''
    returns the winning chocie of the given question
    saves the winning choice to arcieve question table
    
    TODO:
        handle the case when there is no vote in that question
    '''
    cursor = connection.cursor()

    # get the votes
    votes = Vote.objects.raw("SELECT * FROM polls_vote WHERE question_id=%s", [question_id])
    #Vote.objects.filter(question_id=question_id)

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

    #Question.objects.get(id=question_id)
    winning_choice = winning_choices[random.randint(0,len(winning_choices)-1)]

    """
    cursor.execute("INSERT INTO polls_choice"
                    "(question_id, owner_id, place_id, name, votes)"
                    "VALUES (%s, %s, %s, %s, 0)",
                    [question_id, current_user.id, attrs[5], attrs[0]]
                    )

    """
    winning_choice_obj = Choice.objects.raw("SELECT * FROM polls_choice WHERE question_id=%s AND id=%s", [question_id, winning_choice])
    ## insert archieve question in
    print(winning_choice_obj[0].place_id.id)
    cursor.execute("INSERT INTO polls_archive_question"
                   "(question_id, place_id)"
                   "VALUES (%s, %s)",
                   [question_id, winning_choice_obj[0].place_id.place_id])
    #arch_question = Archive_question(question=question, place_id=Choice.objects.get(id=winning_choice).place_id)
    #arch_question.save()
    return winning_choice_obj[0] #Choice.objects.get(id=winning_choice)

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
            # Archive_question.objects.get(question=context["question"])
            archive_place_id = Archive_question.objects.raw("SELECT * FROM polls_archive_question WHERE question_id=%s",[context["question"].id])
            # Place.objects.get(place_id=Archive_question.objects.get(question=context["question"]).place_id.place_id)
            context["winner"] = Place.objects.raw("SELECT * FROM polls_place WHERE place_id=%s",[archive_place_id[0].place_id.place_id])[0]
           
            return context
        
        if context["question"].deadline < timezone.now():
            context["question"].is_active=False
            winner = get_winning_choice(context["question"].id)
            context["winner"] = winner
            context["question"].save()
        
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

#class userStats(generic.DetailView):
#    model=Question
#    template_name='polls/userstats.html'
#    
#def userStatsa(request,question_id):
#    a=0
#    if(a==1):
#        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

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
    cursor = connection.cursor()
    
    ## parse place id 
    place_id=request.POST.get('placeId')
    place = Place.objects.raw("SELECT * FROM polls_place WHERE place_id=%s", [place_id])
    city=request.POST.get('citytable')
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    print(city)

    print("place_id:{}".format(place_id))
    if len(list(place)) == 0:
        print("enetered google api")
        if place_id != "":
            attrs = get_restaurant_attr(place_id)
            attrs.append(city)
        else:
            attrs = [inp_value,"unknown address","unknown phone", 2, 2, "", [""], 0, 0, "www.google.com","unknown city"]
        
        attrs[6] = json.dumps(attrs[6])
        cursor.execute("INSERT INTO polls_place"
                    "(name, address, phone, rating, price_level, place_id, reviews, latitude, longitude, website,city)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                    attrs
                    )
    else: 
        print("existed rest")
        p = place[0]
        attrs = [p.name, p.address, p.phone, p.rating, p.price_level, p.place_id, p.reviews, p.latitude, p.longitude, p.website,p.city]
    generate_wordcloud(place_id, json.loads(attrs[6]), schedule=timezone.now())
    p = subprocess.Popen("./process_tasks.sh", shell=True)

    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")


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
    cursor = connection.cursor()

    # equivlanet in django:
    # q = Question(question_text=inp_value,pub_date=timezone.now(),owner=request.user, deadline=deadline, is_active=True)
    # q.save()
    cursor.execute("INSERT INTO polls_question"
                   "(question_text, pub_date, owner_id, deadline, is_active)"
                   "VALUES (%s, NOW(), %s, %s, 1)",
                   (inp_value, request.user.id, deadline))
    question_id = cursor.lastrowid
    
    # equivalent in django:
    # poll_mem = Poll_members(member=request.user, question=q)
    # poll_mem.save()
    cursor.execute("INSERT INTO polls_poll_members"
                   "(member_id, question_id)"
                   "VALUES (%s, %s)",
                   (request.user.id, question_id))
    
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

    """
    cursor = connection.cursor()
    user = request.user
    inp_value = request.POST.get('name')
    member_id = CustomUser.objects.raw("SELECT * FROM users_customuser WHERE name = %s", [inp_value])
    
    question = Question.objects.raw("SELECT * FROM polls_question WHERE id=%s", [question_id])

    # checking tha onwer is not adding himself or user doesn't exist
    if (len(member_id) != 1):
        return HttpResponseRedirect(reverse('polls:index'))

    check_user_exist = Poll_members.objects.raw("SELECT * FROM polls_poll_members WHERE member_id = %s AND question_id = %s",[member_id[0].id, question_id])
    if (len(check_user_exist) > 0):
        return HttpResponseRedirect(reverse('polls:index'))
    """
    new_member = Poll_members(member=member_id[0], question=question)
    new_member.save()
    """
    cursor.execute("INSERT INTO polls_poll_members"
                   "(member_id, question_id)"
                   "VALUES (%s, %s)",
                   (member_id[0].id, question_id))
    
    return HttpResponseRedirect(reverse('polls:index'))

def get_data(request,*args,**kwargs): 
    inp_value = request.POST.get('city')
    print("testing city")
    city_name=request.GET.getlist('passin')[0]
    print(city_name)
    if city_name:
        print("not empty string")
        cur = connection.cursor()
        cur.execute("SELECT c.name, COUNT(*) FROM polls_vote v, polls_choice c,polls_place p WHERE c.id=v.choice_id AND p.place_id=c.place_id AND p.city=%s GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 5",[city_name])
    else:
        cur = connection.cursor();
        cur.execute("SELECT c.name, COUNT(*) FROM polls_vote v, polls_choice c WHERE c.id=v.choice_id GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 5")
    convert = cur.fetchall()
    data = dict((x, y) for x, y in convert)
    print(data)
    return JsonResponse(data)

def get_mvisited(request,*args,**kwargs):
    inp_value = request.POST.get('city')
    city_name=request.GET.getlist('passin')[0]
    if city_name:
        cur=connection.cursor();
        cur.execute("SELECT aaa.name, COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id FROM (SELECT p.name, p.place_id,a.question_id,p.city FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND aa.city=%s AND vv.choice_id=cc.id) aaa WHERE aaa.owner_id=%s GROUP BY aaa.place_id",[city_name,request.user.id])
    else:
        cur=connection.cursor();
        cur.execute("SELECT aaa.name, COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id FROM (SELECT p.name, p.place_id,a.question_id FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id) aaa WHERE aaa.owner_id=%s GROUP BY aaa.place_id",[request.user.id])
    convert=cur.fetchall()
    mvisited=dict((x, y) for x, y in convert)
    print(mvisited)
    return JsonResponse(mvisited)
    
def get_mvotedx(request,*args,**kwargs):

    inp_value = request.POST.get('city')
    city_name=request.GET.getlist('passin')[0]
    if city_name:
        cur=connection.cursor();
        cur.execute("SELECT g1.aa,g1.bb FROM( SELECT c.name as aa, COUNT(*) as bb, c.question_id as cc FROM polls_vote v, polls_choice c,polls_place p WHERE c.id=v.choice_id AND p.city=%s GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 5 ) g1, polls_question q WHERE g1.cc=q.id and q.pub_date>=DATE_ADD(NOW(),INTERVAL -7 DAY)",[city_name])
    else:
        cur=connection.cursor();
        cur.execute("SELECT g1.aa,g1.bb FROM( SELECT c.name as aa, COUNT(*) as bb, c.question_id as cc FROM polls_vote v, polls_choice c WHERE c.id=v.choice_id GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 5 ) g1, polls_question q WHERE g1.cc=q.id and q.pub_date>=DATE_ADD(NOW(),INTERVAL -7 DAY)")

    convert=cur.fetchall()
    mvotedx=dict((x, y) for x, y in convert)
    print(mvotedx)
    return JsonResponse(mvotedx)
    
def get_mvisitedx(request,*args,**kwargs):
    inp_value = request.POST.get('city')
    city_name=request.GET.getlist('passin')[0]
    cur=connection.cursor();
    if city_name:
        cur.execute("SELECT aaa.name, COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id FROM (SELECT p.name, p.place_id,a.question_id, p.city FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND aa.city=%s AND vv.choice_id=cc.id) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id AND qqq.pub_date>=DATE_ADD(NOW(),INTERVAL -7 DAY) GROUP BY aaa.place_id",[city_name,request.user.id])
    else:
        cur.execute("SELECT aaa.name, COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id FROM (SELECT p.name, p.place_id,a.question_id FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id AND qqq.pub_date>=DATE_ADD(NOW(),INTERVAL -7 DAY) GROUP BY aaa.place_id",[request.user.id])
    convert=cur.fetchall()
    mvisitedx=dict((x, y) for x, y in convert)
    print(mvisitedx)
    return JsonResponse(mvisitedx)

def get_price(request,*args,**kwargs):
    inp_value = request.POST.get('city')
    city_name=request.GET.getlist('passin')[0]
    cur=connection.cursor();
    if city_name:
        cur.execute("SELECT aaa.price_level,COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id, aa.price_level FROM (SELECT p.name, p.place_id,a.question_id, p.price_level, p.city FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id AND aa.city=%s) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id GROUP BY aaa.price_level",[city_name,request.user.id])
    else:
        cur.execute("SELECT aaa.price_level,COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id, aa.price_level FROM (SELECT p.name, p.place_id,a.question_id, p.price_level FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id GROUP BY aaa.price_level",[request.user.id])
    convert=cur.fetchall()
    price=dict((x, y) for x, y in convert)
    
    print(price)
    return JsonResponse(price)    
    
def get_rating(request,*args,**kwargs):
    inp_value = request.POST.get('city')
    city_name=request.GET.getlist('passin')[0]
    cur=connection.cursor();
    if city_name:
        cur.execute("SELECT aaa.rating,COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id, aa.rating FROM (SELECT p.name, p.place_id,a.question_id, p.rating,p.city FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id AND aa.city=%s) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id GROUP BY aaa.rating",[city_name,request.user.id])
    else:
        cur.execute("SELECT aaa.rating,COUNT(*) FROM(SELECT aa.name, aa.place_id,cc.owner_id,aa.question_id, aa.rating FROM (SELECT p.name, p.place_id,a.question_id, p.rating FROM polls_archive_question a INNER JOIN polls_place p ON a.place_id=p.place_id) aa, polls_choice cc, polls_vote vv WHERE cc.place_id=aa.place_id AND vv.choice_id=cc.id) aaa, polls_question qqq WHERE aaa.owner_id=%s AND qqq.id=aaa.question_id GROUP BY aaa.rating",[request.user.id])
    convert=cur.fetchall()
    rating=dict((x, y) for x, y in convert)
    print(rating)
    return JsonResponse(rating)    
    