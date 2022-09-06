from http.client import HTTPResponse
from typing import Type
from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    information = forms.CharField(widget=forms.Textarea,label="Information")


def htmlconvert(title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    html = markdowner.convert(entry)

    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
#SEARCH
def searchbar(s):
    # CASEFOLD THE LIST AND DEVIDE IT INTO LIST OF LISTS WITH LETTERS
    letters_list = [list(map(str.casefold, x)) for x in util.list_entries()]
    for word in letters_list:
        if len(s) == 1:
            if s in word:
                return(word)

        elif len(s) > 1:
                x = ''.join(word)

                print("x is ", x) # TEST, Remove later
                
                if x.find(s) != -1:
                        return x


def search(request):
    
    if request.method == 'POST':
        searched = request.POST["q"]
        
        print("REQURDT METHOD:",request.method)
        print("SEARCHED:",searched)
    try:    
       
        #if (''.join(searchbar(searched))):
         
        x = ''.join(searchbar(searched))
        print( "SEARCHBAR:",x )

        return render(request, "encyclopedia/search.html", {
            "searched": searched, "entries": x, "entry":x.upper()
        })
    except TypeError:
#else:
        return render(request, "encyclopedia/search.html", {
            "searched": searched, "entries":util.list_entries()
        })



# LIST_ENTRIES :  ['CSS', 'Django', 'Git', 'HTML', 'Python']
#def entry(request):
#    ...
        



def new(request):   

    form = EntryForm(request.POST)
    if form.is_valid():

        title = form.cleaned_data['title']
        information = form.cleaned_data['information']
            
        print("Title",title,"Info:",information)
    return render(request, "encyclopedia/new.html",{
        "form":form
    })



