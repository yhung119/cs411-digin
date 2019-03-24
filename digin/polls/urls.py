from django.urls import path
from rest_framework import routers
from .api import QuestionViewSet, ChoiceViewSet, UserViewSet
from . import views


router = routers.DefaultRouter()
router.register('api/questions', QuestionViewSet, 'questions')
router.register('api/choices', ChoiceViewSet, 'choices')
router.register('api/users', UserViewSet, 'users')

urlpatterns = router.urls
