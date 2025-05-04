from re import sub, template
from typing import Text
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
import markdown
import random

from . import util

class SearchForm(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}), label='')

class CreateForm(forms.Form):
    page_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'create_holder', 'placeholder': 'Title'}), label='')
    create_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'create_holder', 'placeholder': 'Content'}), label='')

class EditForm(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'create_holder'}), label='')

def index(request):
    entries = util.list_entries()
    possible_entries = []
    #if request method is POST
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            for i in entries:
                if item.lower() == i.lower():
                    return redirect(f'wiki/{i}')
                if item.lower() in i.lower():
                    possible_entries.append(i)
            if(len(possible_entries)>0):
                return render(request, "encyclopedia/search.html", {
                    "possible_entries": possible_entries,
                    "search_form": SearchForm()
                })
            else:
                return render(request, "encyclopedia/PageDoesntExist.html",{
                    "template_name": item,
                    "search_form": SearchForm()
                })
    #if request method is GET or other methods
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "search_form": SearchForm()
    })
        
def entry(request, template_name):
    md = markdown.Markdown()
    entry_in_md = util.get_entry(template_name)
    if entry_in_md is None:
        return render(request, "encyclopedia/PageDoesntExist.html", {
            "template_name": template_name,
            "search_form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(entry_in_md),
            "template_name": template_name,
            "search_form": SearchForm()
        })

def create(request):
    all_entries = util.list_entries()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data['page_title']
            create_content = form.cleaned_data['create_content']
            for i in all_entries:
                if page_title.lower() == i.lower():
                    return render(request, "encyclopedia/PageAlreadyExist.html",{
                        "search_form": SearchForm(),
                        "template_name": i
                    })
            util.save_entry(page_title, create_content)
            return render(request, 'encyclopedia/PageSuccessfullyAdd.html', {
                "search_form": SearchForm(),
                "title": page_title
            })
    
    else:
        return render(request, "encyclopedia/create.html", {
            "create_form": CreateForm(),
            "search_form": SearchForm()
        })

def edit(request, template_name):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            edit_content = form.cleaned_data['edit_content']
            util.save_entry(template_name, edit_content)
            return entry(request, template_name)
    else:
        content = util.get_entry(template_name)
        return render(request, "encyclopedia/edit.html", {
            "search_form": SearchForm(),
            "edit_form": EditForm(initial={'edit_content': content}),
            "template_name": template_name
        })

def rand(request):
    ls = util.list_entries()
    n = random.randint(0,len(ls)-1)
    return entry(request, ls[n])