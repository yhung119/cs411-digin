from django.conf.urls import url
from django.urls import path

from . import views
from .views import get_data,get_mvisited, get_mvotedx,get_mvisitedx,get_price,get_rating

app_name = 'polls'
urlpatterns = [\
    path('', views.IndexView.as_view(), name='home'),
	
	url(r'^api/data/$', get_data, name='api-data'),#for graph data
	url(r'^api/mvisited/$', get_mvisited, name='api-mvisited'),#for graph data
	url(r'^api/mvotedx/$', get_mvotedx, name='api-/mvotedx'),#for graph data
	url(r'^api/mvisitedx/$', get_mvisitedx, name='api-/mvisitedx'),#for graph data
	url(r'^api/price/$', get_price, name='api-/price'),#for graph data
	url(r'^api/rating/$', get_rating, name='api-/price'),#for graph data
	#url(r'^(?P<pk>[0-9]+)/userstats$', views.userStats.as_view(), name='userstats'),
	#url(r'^(?P<question_id>[0-9]+)/userStatsa/$', views.userStatsa, name='userStatsa')
	
    path('polls/', views.IndexView.as_view(), name="index"),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^(?P<question_id>[0-9]+)/delQuestion/$', views.delQuestion, name='delQuestion'),
    #url(r'^(?P<choice_id>[0-9]+)/(?P<question_id>[0-9]+)/delChoice/$', views.delChoice, name='delChoice'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/addChoice/$', views.addChoice, name='addChoice'),
    
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    url(r'^(?P<question_id>[0-9]+)/editQuestion/$', views.editQuestion, name='editQuestion'),

    url(r'^(?P<pk>[0-9]+)/add/$', views.AddUserView.as_view(), name='add'),
    url(r'^(?P<question_id>[0-9]+)/addUser/$', views.addUser, name='addUserAPI'),
]