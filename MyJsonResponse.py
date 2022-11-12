from django.http import JsonResponse

def jres(isSuccess, dataToSend = None):
    successOrFail = 'Success' if isSuccess else 'Fail'
    return JsonResponse({'message':successOrFail}, data = dataToSend, status=200)