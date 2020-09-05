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

def search(request):
        all_titles = util.list_entries()
        partial_matches = []
        for title in all_titles:
            if title.lower() == request.GET["q"].lower():
                # potential for optimisation here...
                return render(request, "encyclopedia/wiki.html", {
                    "title": title,
                    "entry": util.get_entry(title)
                    })
            elif request.GET["q"].lower() in title.lower():
                partial_matches.append(title)
            else:
                continue
        if len(partial_matches) > 0:
            return render(request, "encyclopedia/search.html", {
                "partial_matches": partial_matches
            })
        else:
            # No matches at all
            print("No Match")
        
        return render(request, "encyclopedia/search.html")