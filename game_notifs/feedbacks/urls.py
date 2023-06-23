from django.urls import path
from .views import *

urlpatterns = [
    path('', FeedbackView.as_view(), name="give_get_feedback"),
    path('feedback_wall/', FeedbackWallView.as_view(), name="feedback_wall"),
    path('update_feedback/<int:pk>/', UpdateFeedback.as_view(), name="update_feedback"),
    path('delete_feedback/<int:pk>/', DeleteFeedback.as_view(), name="delete_feedback"),
]