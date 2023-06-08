from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel

# Create your models here.
class FeedbackModel(BaseModel):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=300, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.feedback
    