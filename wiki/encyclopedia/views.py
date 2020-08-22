from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    print(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if title.lower() in map(lambda x:x.lower(), util.list_entries()):
       return render(request, "encyclopedia/wiki.html", {
           "title": title
        })
    else:
        return HttpResponse("<h1>Page not yet created</h1>") 