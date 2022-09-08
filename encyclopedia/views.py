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
    form = EntryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['title']
            information = form.cleaned_data['information']
            print(form.cleaned_data["edit"], "FORM VALID")
            print("TITLE", title, "INFORMATION", information)
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                print(form.cleaned_data['edit'])
                util.save_entry(title,information)
                return render(request, "encyclopedia/entry.html",{
                    "content": htmlconvert(title), "entry": title
                })

            return HttpResponse("PAGE ALREADY EXISTS") # CHANGE THIS
    else:
        return render(request, "encyclopedia/new.html",{
           "form":form,
            "existing": False,
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
        form.fields["edit"].initial == True
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
                    print("LIST_LETTERS: ",list_words)
            return render(request, "encyclopedia/search.html",{
                "entries":list_words,
                "entry" : entry,
                "searched": searched
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