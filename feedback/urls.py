#from django.urls import path
#from .views import (
  #  get_feedback, add_feedback, register_student,
 #   login_student, add_institution
#)

#urlpatterns = [
 #   path('feedback/', get_feedback, name='get_feedback'),
#   path('feedback/add/', add_feedback, name='add_feedback'),
#  path('students/register/', register_student, name='register_student'),
 #   path('students/login/', login_student, name='login_student'),
 #   path('institutions/add/', add_institution, name='add_institution'),
#]

from django.urls import path
from .views import (
    register_student,
    login_student, register_institution, login_institution, submit_feedback, view_feedback, view_student_feedback, predict_sentiment, 
    institution_overall_sentiment,category_wise_sentiment,student_sentiment_distribution
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Registration & Login Endpoints
    path('register/', register_student, name='register'),
    path('login/', login_student, name='login'),

    # JWT Token Management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Institution APIs
    path('institution/register/', register_institution, name='register_institution'),
    path('institution/login/', login_institution, name='login_institution'),

    # Feedback Submission
    path('feedback/submit/', submit_feedback, name='submit_feedback'),
    path('institution/view-feedback/', view_feedback, name='view_feedback'),#view feedback for institution
    path('student/view-feedback/', view_student_feedback, name='view_student_feedback'),#view feedback for students

    path('predict-sentiment/', predict_sentiment, name='predict_sentiment'),
    path('institution-overall-sentiment/', institution_overall_sentiment, name='institution_overall_sentiment'),
    path('category-wise-sentiment/', category_wise_sentiment, name='category_wise_sentiment'),
    path('student-sentiment-distribution/', student_sentiment_distribution, name='student_sentiment_distribution'),
]


