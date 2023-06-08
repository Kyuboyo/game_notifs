from .models import FeedbackModel
from django.core.serializers import serialize

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
    return json.dumps(list(FeedbackModel.objects.filter(deleted_at__isnull = True).values('feedback')[:20]))