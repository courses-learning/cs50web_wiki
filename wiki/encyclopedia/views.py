from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django import forms

from random import randrange

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Title")
    markup = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), label="")


class EditEntryForm(forms.Form):
    markup = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if title.lower() in map(lambda x:x.lower(), util.list_entries()):
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
            # Searched title already exists -> goto page
            if title.lower() == request.GET["q"].lower():
                return redirect('wiki', title)
            # Partial match found against current iterable -> add to partial_match list
            elif request.GET["q"].lower() in title.lower():
                partial_matches.append(title)
            # No match current iterable
            else:
                continue
        
        return render(request, "encyclopedia/search.html", {
            "partial_matches": partial_matches
        })


def new(request):

    # POST so submission of new title/entry has occurred
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markup = form.cleaned_data["markup"]

            # new title already exists
            if title.lower() in map(lambda x:x.lower(), util.list_entries()):
                messages.info(request, 'Already an entry for this')
                return HttpResponseRedirect(reverse("index"))
            # Create new title/entry, save and goto that new page
            else:
                util.save_entry(title, markup)
                return redirect('wiki', title)

        # Catch if form POST with invalid data 
        else:
            return HttpResponse("<h1>Something went wrong - Invalid data submitted</h1>") 

    # Initial load via GET so render blank form
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })


def random(request):
    all_titles = util.list_entries()
    rand_title = all_titles[randrange(len(all_titles))]
    return redirect('wiki', rand_title)


def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            markup = form.cleaned_data["markup"]
            util.save_entry(title, markup)
            return redirect('wiki', title)
        else:
            return HttpResponse("<h1>Something went wrong - Invalid data submitted</h1>") 
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": EditEntryForm({'markup': util.get_entry(title)})
        })
    