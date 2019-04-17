from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse

from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone
from django.db import connection
from django.db.models.expressions import RawSQL


class HomePageView(TemplateView):
    template_name = 'home.html'

class IndexView(generic.ListView):
    
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    # @login_required
    def get_queryset(self):
        # print(self.request.user)
        """Return the last five published questions."""
        return Question.objects.raw("SELECT * FROM polls_question ORDER BY pub_date DESC")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        ## the context is a list of the tasks of the Project##
        ##THIS IS THE ERROR##
        context['choices'] = Choice.objects.raw("SELECT * FROM polls_choice WHERE question_id = %s",[context["question"].id])
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class EditView(generic.DetailView):
    model = Question
    template_name = 'polls/edit.html'

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
	inp_address=request.POST.get('address')
	inp_placeid=request.POST.get('placeid')
	
	try:
		question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO polls_choice"
				"(choice_text, votes, owner_id, question_id)"
				"VALUES (%s, %s, %s, %s)",
				[inp_value, 0, request.user.id, question_id]
				)
	# question.choice_set.create(choice_text=inp_value,votes=0,owner=request.user)
	return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
	
def addQuestion(request):
    inp_value = request.POST.get('question')
    # q = Question(question_text=inp_value,pub_date=timezone.now(),owner=request.user)
    # q.save()
	
    cursor = connection.cursor()
    cursor.execute("INSERT INTO polls_question"
                   "(question_text, pub_date, owner_id)"
                   "VALUES (%s, NOW(), %s)",
                   (inp_value, request.user.id)
                   )
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
    
#def delChoice(request,choice_id,question_id):
#   print("deleteChoice")
#   question = get_object_or_404(Question, pk=question_id)
#   choice = get_object_or_404(Choice, pk=choice_id)
#   choice.delete()
#   
#   return HttpResponseRedirect(reverse('polls:vote', args=(question.id,)))
#************goes in details.html
#<form method="post" action="{% url 'polls:delChoice' choice.id question.id%}" >
#   {% csrf_token %}
#   <input type="submit" value="x">
#</form>

def editQuestion(request,question_id):
    try:
        question = Question.objects.raw("SELECT * FROM polls_question WHERE id = %s", [question_id])[0]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    inp_value=request.POST.get('choice')
    cursor = connection.cursor()
    cursor.execute("UPDATE polls_question SET question_text = %s WHERE id=%s AND owner_id=%s", [inp_value, question_id, request.user.id])
    return HttpResponseRedirect(reverse('polls:index'))

def get_data(request,*args,**kwargs):
	print("hello")
	cur=connection.cursor();
	cur.execute("SELECT c.choice_text, COUNT(*) FROM polls_vote v, polls_choice c WHERE c.id=v.choice_id GROUP BY c.choice_text ORDER BY COUNT(*) DESC LIMIT 5")
	convert=cur.fetchall()
	data=dict((x, y) for x, y in convert)
	print(data)
	return JsonResponse(data)