from django.urls import path
from .views import *

urlpatterns = [
    path('', FeedbackView.as_view(), name="give_get_feedback"),
    path('feedback_wall/', FeedbackWallView.as_view(), name="feedback_wall"),
]