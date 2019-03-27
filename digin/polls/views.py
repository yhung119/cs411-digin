from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone
from django.db import connection


class HomePageView(TemplateView):
	template_name = 'home.html'

class IndexView(generic.ListView):
	
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	# @login_required
	def get_queryset(self):
		# print(self.request.user)
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

class EditView(generic.DetailView):
	model = Question
	template_name = 'polls/edit.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		try:
			Vote.objects.get(question=question, owner=request.user, choice=selected_choice)
		except(Vote.DoesNotExist):	
			selected_choice.votes += 1
			selected_choice.save()
			v=Vote(question=question,owner=request.user,choice=selected_choice)
			v.save()
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
		else:
			return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You have already voted.",
		})

		
def addChoice(request, question_id):
	print("choice")
	current_user=request.user
	print(current_user.id)
	question = get_object_or_404(Question, pk=question_id)
	inp_value = request.POST.get('choice')

	question = get_object_or_404(Question, pk=question_id)
	question.choice_set.create(choice_text=inp_value,votes=0,owner=request.user)
	return HttpResponseRedirect(reverse('polls:vote', args=(question.id,)))
	
def addQuestion(request):
	print("question")
	inp_value = request.POST.get('question')
	print(request.user)
	q = Question(question_text=inp_value,pub_date=timezone.now(),owner=request.user)
#cursor.execute("INSERT INTO polls_question"
#               "(password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, name)"
#               "VALUES (%s, 0, %s, '', '', %s, 0, 1, NOW(), %s)",
#               (make_password(validated_data["password"]), validated_data["username"], validated_data["email"], validated_data["name"])
#    )
	q.save()
	return HttpResponseRedirect(reverse('polls:index'))

def delQuestion(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	question.delete()
	print("delete")
	return HttpResponseRedirect(reverse('polls:index'))
	
#def delChoice(request,choice_id,question_id):
#	print("deleteChoice")
#	question = get_object_or_404(Question, pk=question_id)
#	choice = get_object_or_404(Choice, pk=choice_id)
#	choice.delete()
#	
#	return HttpResponseRedirect(reverse('polls:vote', args=(question.id,)))
#************goes in details.html
#<form method="post" action="{% url 'polls:delChoice' choice.id question.id%}" >
#	{% csrf_token %}
#	<input type="submit" value="x">
#</form>	
def editQuestion(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	inp_value=request.POST.get('choice')
	print(inp_value)
	question.question_text=inp_value
	print(question.question_text)
	question.save()
	return HttpResponseRedirect(reverse('polls:index'))