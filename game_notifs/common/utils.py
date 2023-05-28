from django.http.response import JsonResponse
from copy import deepcopy


responseSchema = {
    'status': '',
    'data': None,
    'message': '',
    'error_message': '',
}

def sendResponse(statusCode, responseData, toJson=True, mimetype='application/json', responseHeaders=None):
    try:
        response = JsonResponse(
            safe=False, status=statusCode, data=responseData)
        if (responseHeaders is not None):
            for k, v in responseHeaders.items():
                response[k] = v
        return response
    except Exception as e:
        res = deepcopy(responseSchema)
        res['status'] = "Failed"
        res['error_message'] = str(e)
        return JsonResponse(safe=False, status=500, data=res)
