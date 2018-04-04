# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import string

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from Shotter import settings
from .models import Urls
# Create your views here.
import urllib2
import requests
from django.http import JsonResponse

def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not        found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)


class Count(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data.copy()
        print data['short_url'][15:]
        url = get_object_or_404(Urls, pk=data['short_url'][15:])
        response_data = {}
        response_data['count'] =  url.count
        response_data['status'] ='OK'
        response_data['status_codes'] =[]
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_urls(self):
    Urls.objects.all().delete()

    return JsonResponse({'status':'OK'},status=200)





























class Longer(APIView):

    permission_classes = [AllowAny]
    def post(self, request, format=None):
     data = request.data.copy()
     print data['short_url'][15:]


     try:
          url = get_object_or_404(Urls, pk=data['short_url'][15:])
          url.count += 1
          url.save()
          response_data = {}
          response_data['long_url'] =  url.httpurl
          response_data['status'] ='OK'
          response_data['status_codes'] =[]
          return HttpResponse(json.dumps(response_data), content_type="application/json")
     except requests.ConnectionError:
       return HttpResponse(json.dumps({"status": "FAILED"},{"status_codes":"SHORT_URLS_NOT_FOUND"}), content_type="application/json")

class Shorten(APIView):
    queryset = Urls.objects.all()

    permission_classes = [AllowAny]

    def post(self, request, format=None):
     data = request.data.copy()
     url=data['long_url']
     if not (url == ''):
        short_id = get_short_code()
        b = Urls(httpurl=url, short_id=short_id)
        b.save()

        response_data = {}
        response_data['short_url'] =  settings.SITE_URL +"/" + short_id
        response_data['status'] ='OK'
        response_data['status_codes'] =[]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
     return HttpResponse(json.dumps({"status": "FAILED"},{"status_codes": "INVALID_URLS"}), content_type="application/json")


class ShortenList(APIView):
    queryset = Urls.objects.all()

    permission_classes = [AllowAny]

    def post(self, request, format=None):
     data = request.data.copy()
     urls=data['long_urls']

     response_data = {}
     failed_response={}
     failed_response['status']= "FAILED"
     failed_response['status_codes']= "INVALID_URLS"
     response_data['short_urls'] =  {}
     response_data['status'] ='OK'
     response_data['status_codes'] =[]
     response_data['invalid_urls'] =[]
     failed_urls=[]
     for url in urls:

      if not (url == ''):
        try:
             r = requests.head(url)
             if r.status_code== 200:
              short_id = get_short_code()
              b = Urls(httpurl=url, short_id=short_id)
              print url
              response_data['short_urls'][url]=settings.SITE_URL +"/" + short_id
              b.save()
             else:
                 failed_urls.append(url)
        except requests.ConnectionError:
            failed_urls.append(url)
     if len(failed_urls)>0:
         failed_response['invalid_urls']=failed_urls
         return HttpResponse(json.dumps(failed_response), content_type="application/json")

     else:
         return HttpResponse(json.dumps(response_data), content_type="application/json")




class LongerList(APIView):
    queryset = Urls.objects.all()

    permission_classes = [AllowAny]

    def post(self, request, format=None):
     data = request.data.copy()
     urls=data['short_urls']

     response_data = {}
     failed_response={}
     failed_response['status']= "FAILED"
     failed_response['status_codes']= "SHORT_URLS_NOT_FOUND"
     response_data['long_urls'] =  {}
     response_data['status'] ='OK'
     response_data['status_codes'] =[]
     response_data['invalid_urls'] =[]
     failed_urls=[]
     for uri in urls:

      if not (uri == ''):
        try:
            url = get_object_or_404(Urls, pk=uri[15:])
            url.count += 1
            url.save()
            response_data['long_urls'][uri]=url.httpurl





        except:
            failed_urls.append(uri)
     if len(failed_urls)>0:
         failed_response['invalid_urls']=failed_urls
         return HttpResponse(json.dumps(failed_response), content_type="application/json")

     else:
         return HttpResponse(json.dumps(response_data), content_type="application/json")




def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id