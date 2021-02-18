from django.shortcuts import render
import json
import requests
from rest_framework.response import Response
from django.http import HttpResponse
import time


def AsyncTask(keyword, podcast_id):
    countries = ["us", "ca", "sg", "in", "cn", "au", "ue"]

    res = []
    urls = []
    for country in countries:
        url = f"https://itunes.apple.com/search?term={keyword}&entity=podcast&country={country}"
        urls.append(url)

    for i in range(len(countries)):
        country = countries[i]
        url = urls[i]
        try:
            rank = 100000
            r = requests.get(url)
            r = json.loads(r.content)
            results = r["results"]
            n = len(results)
            for idx in range(n):
                # print(type(results[idx]["trackId"]), type(podcast_id))
                if results[idx]["trackId"] == podcast_id:
                    res.append({"country": country, "search_rank": idx+1})
                    # rank = idx+1
                    break
        except:
            rank = 100000
            res.append({"country": country, "search_rank": rank})

    return res


def SeoReportView(request):
    if request.method == "GET":
        # print(request.body)
        # json_data = json.loads(request.body)
        # keyword = json_data['keyword']
        # podcast_id = json_data['podcast_id']

        keyword = request.GET.get('keyword')
        podcast_id = request.GET.get('podcast_id')
        # time.sleep(5)

        podcast_id = (int)(podcast_id)
        # print('[KEYWORD]', keyword)
        # print('[PODCAST_ID]', type(podcast_id))

        res = AsyncTask(keyword, podcast_id)

        return HttpResponse(json.dumps(res), content_type="application/json")

# 1524711606
