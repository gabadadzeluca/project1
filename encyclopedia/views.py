from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from random import choice

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    information = forms.CharField(widget=forms.Textarea,label="Information")
    edit = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

def htmlconvert(title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    html = markdowner.convert(entry)
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    




def new(request):   
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            information = form.cleaned_data['information']
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,information)
                return render(request, "encyclopedia/entry.html",{
                    "content": htmlconvert(title), "entry": title,
                    
                })
            # IF THE PAGE EXISTS ALREADY
            return render(request,"encyclopedia/entry.html",{
                "entry":title,
                "message":"Page Already Exists, press the button to Edit",
                "existing":True

            })
    else:
        return render(request, "encyclopedia/new.html",{
            "form":EntryForm(),
            #"existing": False,
        })


def edit(request,entry):
    entryPage = util.get_entry(entry)
   
    if entryPage is None:
        return render(request, "encyclopedia/nonExisting.html",{
            "entry":entry
        })
    else:
        form = EntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget=forms.HiddenInput()
        form.fields["information"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/edit.html",{
            "form": form,
            "title" : form.fields["title"].initial,
            "edit" : form.fields["edit"].initial
       })


def entry(request, entry):
   
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request,"encyclopedia/nonExisting.html",{
            "entry":entry
        })
    return render(request, "encyclopedia/entry.html",{
            "content":htmlconvert(entry), "entry":entry
    })


def search(request):
    if request.method == "GET":
        list_words = []
        searched = request.GET.get('q')
        if util.get_entry(searched) is None:
            for entry in util.list_entries():
                if searched.upper() in entry.upper():
                    list_words.append(entry)
            
            if len(list_words) == 0:
                return render(request, "encyclopedia/search.html",{
                    "entries": list_words,
                    "entry":entry,
                    "searched":searched,
                    "existing": False
                })
            return render(request, "encyclopedia/search.html",{
                "entries":list_words,
                "entry" : entry,
                "searched": searched,
                "existing": True
            })
        if util.get_entry(searched) is not None:
            return render(request,"encyclopedia/entry.html",{
                "entry": searched,
                "content": htmlconvert(searched)
            })



def random(request):
    entry = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html",{
        "entry": entry,
        "content": htmlconvert(entry)
    })