from django.shortcuts import render
import json
import requests
from rest_framework.response import Response
from django.http import HttpResponse
import time
import os
from operator import itemgetter


def GetAllCountries():
    try:
        filename = open(os.getcwd()+"/api/countries.json",)
    except:
        print(os.getcwd())

    countries = json.load(filename)
    filename.close()
    return countries


def AsyncTask(keyword, podcast_id):
    # countries = ["us", "ca", "sg", "in", "cn", "au", "ue"]
    countries = GetAllCountries()

    res = []
    urls = []
    for country in countries:
        url = f"https://itunes.apple.com/search?term={keyword}&entity=podcast&country={countries[country]}"
        urls.append(url)

    i = 0
    for country in countries:
        url = urls[i]
        i += 1
        try:
            rank = 100000
            r = requests.get(url)
            r = json.loads(r.content)
            results = r["results"]
            n = len(results)
            ok = 0
            for idx in range(n):
                if results[idx]["trackId"] == podcast_id:
                    res.append({"country": country, "search_rank": idx+1})
                    ok = 1
                    break
            if ok == 0:
                res.append({"country": country, "search_rank": rank})
        except:
            rank = 100000
            res.append({"country": country, "search_rank": rank})

    newlist = sorted(res, key=itemgetter("search_rank"))
    response = []

    for i in range(20):
        response.append(newlist[i])

    return response


def SeoReportView(request):
    if request.method == "GET":

        keyword = request.GET.get('keyword')
        podcast_id = request.GET.get('podcast_id')

        podcast_id = (int)(podcast_id)

        res = AsyncTask(keyword, podcast_id)

        return HttpResponse(json.dumps(res), content_type="application/json")

# 1524711606
