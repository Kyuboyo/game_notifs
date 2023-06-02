from django.shortcuts import render
from rest_framework.views import APIView

from .service import *
from common.utils import responseSchema, sendResponse
from copy import deepcopy

class OffersView(APIView):
    def get(self, request):
        res = deepcopy(responseSchema)
        try:
            data = get_free_games('epic')
            res['status']   = "Success"
            res['message']  = "Logged out successfully"
            res['data']     = data
            return render(request, "index2.html", {"data":data})
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)

    
class PullData(APIView):
    def get(self, request):
        res = deepcopy(responseSchema)
        try:
            fresh_data = pull_free_games_epic('epic')
            # compare fresh data with cache and if it doesn't  match then save in DB
            cache_data = get_cached_data('epic')
            fresh_data_titles, cache_data_titles = compare_cache_with_data(fresh_data, cache_data)
            if fresh_data_titles != cache_data_titles:
                save_offers(fresh_data, 'epic')
                update_cached_data('epic')
            res['status']   = "Success"
            res['message']  = "Data updated successfully"
            return sendResponse(200, res)
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)

class StoreToEmptyDB(APIView):
    def get(self, request):
        res = deepcopy(responseSchema)
        try:
            data = pull_free_games_epic('epic')
            save_offers(data, 'epic')
            res['status']   = "Success"
            res['message']  = "Logged out successfully"
            return sendResponse(200, res)
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)
