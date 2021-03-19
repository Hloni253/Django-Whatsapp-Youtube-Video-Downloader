from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from youtube_search import YoutubeSearch
from .models import YoutubeUrl
import os
import re

tube_file_url = ""
search_name = ""
num = ""


def HomePage(request):
    global tube_file_url
    if request.method == "POST":
        message = request.POST.get("Search")
        mess_to_string = str(message)
        for url in YoutubeUrl.objects.all():
            if mess_to_string.startswith(url.verification_url):
                tube_file_url = mess_to_string.replace(url.verification_url,"")
                return redirect("/Download/Download")
        return redirect("/")
    else:
        pass
    
    return render(request, "Home/Home.html")


@csrf_exempt
def Webhook(request):
    global tube_file_url
    global search_name
    global num
    
    response = MessagingResponse()
    msg = response.message()
    if request.method == "POST":
        message = request.POST.get("Body")
        try:
            int(message)
            num = int(message)
            results = YoutubeSearch(search_name, max_results=10).to_dict()
            num = num - 1
            result = results[num]['url_suffix']
            tube_file_url = result.replace("/watch?v=","")
            msg.body("")#Domain Name

        except ValueError:
            mess_to_string = str(message)
            string_verification = False

            for url in YoutubeUrl.objects.all():
                if mess_to_string.startswith(url.verification_url):
                    tube_file_url = mess_to_string.replace(url.verification_url,"")
                    msg.body("")#Domain Name
                    string_verification = True
                    break

            if string_verification == False:
                results = YoutubeSearch(message, max_results=10).to_dict()
                search_name = message
                for index in range(10):
                    result = results[index]['title']
                    msg.body('--\n{0} {1}\n--'.format(index+1,result))
    
    return HttpResponse(response.to_xml(), content_type='text/xml')


def Download(request):
    global tube_file_url
    
    download_url = "https://www.youtubepp.com/watch?v={}".format(tube_file_url)

    context = {
        "download":download_url
        }

    return render(request, "Home/Download.html", context)
