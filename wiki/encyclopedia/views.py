from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if title.lower() in map(lambda x:x.lower(), util.list_entries()):
        print(util.get_entry(title))
        return render(request, "encyclopedia/wiki.html", {
           "title": title,
           "entry": util.get_entry(title)
        })
    else:
        return HttpResponse("<h1>Page not yet created</h1>") 