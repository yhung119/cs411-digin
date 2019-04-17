from django.conf.urls import url
from django.urls import path

from . import views
from .views import get_data

app_name = 'polls'
urlpatterns = [\
    path('', views.IndexView.as_view(), name='home'),
	url(r'^api/data/$', get_data, name='api-data'),#for graph data
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