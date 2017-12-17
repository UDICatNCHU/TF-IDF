# -*- coding: utf-8 -*-
from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from udicTfidf import TFIDF
from udic_nlp_API.settings_database import uri
obj = TFIDF(uri=uri)

@queryString_required(['keyword'])
def idf(request):
    keyword = request.GET['keyword']
    return JsonResponse(obj.idf(keyword), safe=False)

def tfidf(request):
    if request.POST and 'doc' in request.POST:
        doc = request.POST.dict()['doc']
        try:
            return JsonResponse(obj.tfidf(doc), safe=False)
        except Exception as e:
		    return JsonResponse([], safe=False)        	
    return JsonResponse([], safe=False)