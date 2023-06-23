from .models import FeedbackModel
from django.core.serializers import serialize
from datetime import datetime
import json

def get_feedbacks(user=None):
    if user:
        data = get_my_feedbacks(user)
    else:
        data = get_all_feedbacks()
    
    return json.loads(data)
    
    
def get_my_feedbacks(user):
    return serialize("json",FeedbackModel.objects.filter(
                                            user = user,
                                            deleted_at = None
                                        ))

def get_all_feedbacks():
    datas = FeedbackModel.objects.filter(deleted_at__isnull = True).values('feedback')[:20]
    return json.dumps([data.get('feedback') for data in datas])

def update_feedback(pk, feedback, desc):
    data = FeedbackModel.objects.filter(pk=pk).first()
    if feedback:
        data.feedback = feedback
    if desc:
        data.description = desc
    data.save()

def delete_feedback(pk):
    data = FeedbackModel.objects.filter(pk=pk).first()
    data.deleted_at = datetime.now()
    data.save()