# -*- coding: utf-8 -*-
from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from udicTfidf import TFIDF
from udic_nlp_API.settings_database import uri

multilanguage_model = {
    'zh': TFIDF('zh', uri=uri)
}

@queryString_required(['lang', 'keyword'])
def idf(request):
	lang = request.GET['lang']
	keyword = request.GET['keyword']
	return JsonResponse(multilanguage_model[lang].idf(keyword), safe=False)

@queryString_required(['lang'])
def tfidf(request):
	lang = request.GET['lang']
	if request.POST and 'doc' in request.POST:
		doc = request.POST.dict()['doc']
		flag = request.GET['flag'] if 'flag' in request.GET else None
		return JsonResponse(multilanguage_model[lang].tfidf(doc, flag), safe=False)
	return JsonResponse([], safe=False)