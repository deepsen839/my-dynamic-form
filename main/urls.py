from django.urls import path
<<<<<<< HEAD
from .views import RespondView,SurveyResponseUpdateView,update_events,get_events
=======
from .views import RespondView,SurveyResponseUpdateView,add_form
>>>>>>> fb66ad2b2a661cd05225796ce25ecb8627f96e17

urlpatterns = [
    path('respond/<int:survey_id>/', RespondView.as_view(), name='respond'),
    path('respond/<int:pk>/edit/', SurveyResponseUpdateView.as_view(), name='survey_response_update'),
<<<<<<< HEAD
    path('update-events/',update_events,name='update-events'),
    path('play-events/',update_events,name='update-events'),
    path('get-events/',get_events,name='get-events'),
=======
    path('add-form/', add_form, name='add-form'),
>>>>>>> fb66ad2b2a661cd05225796ce25ecb8627f96e17
]