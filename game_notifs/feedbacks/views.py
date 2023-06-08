from django.shortcuts import render
from rest_framework.views import APIView
from .models import FeedbackModel
from .service import get_feedbacks

from common.utils import responseSchema, sendResponse
import copy


class FeedbackView(APIView):
    def post(self, request):
        # give feedback
        res = copy.deepcopy(responseSchema)
        try:
            user            = request.user
            feedback        = request.POST.get('feedback')
            description     = request.POST.get('description') or ''

            FeedbackModel.objects.create(
                                            user            = user,
                                            feedback        = feedback,
                                            description     = description
                                        )
            res['status']   = "Success"
            res['message']  = "Feedback sent successfully"
            return render(request, "index2.html")
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)
    
    def get(self, request):
        # get feedback
        res = copy.deepcopy(responseSchema)
        try:
            user = request.user
            
            data = get_feedbacks(user)
            res['status']   = "Success"
            res['message']  = "Feedbacks retrieved successfully"
            res['data']     = data
            return render(request, "feedback.html", {"data":data})
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)
        
class FeedbackWallView(APIView):
    def get(self, request):
        # get feedback
        res = copy.deepcopy(responseSchema)
        try:
            data = get_feedbacks()
            res['status']   = "Success"
            res['message']  = "Feedbacks retrieved successfully"
            res['data']     = data
            return render(request, "feedback.html", {"data":data})
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)