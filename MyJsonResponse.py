from django.http import JsonResponse
import json

def jres(isSuccess,data = None):
    successOrFail = 'Success' if isSuccess else 'Fail'
    retData = {}
    retData['message'] = successOrFail
    retData['data'] = data
    return JsonResponse(data = retData, status=200)