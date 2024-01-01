from django.shortcuts import render
import markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, 'encyclopedia/error.html',{
            "msg": "Page not found"
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            "title":title,
            "content":html_content})
    
def search(request):
    if request.method == "POST":
        search_result = request.POST['q']
        search_content = convert_md_to_html(search_result)
        if search_content is not None:
            return render(request, 'encyclopedia/entry.html', {
                "title":search_result,
                "content":search_content})
        else:
            entry_list = util.list_entries()
            recomendation = []
            for entry in entry_list:
                if search_result.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request, 'encyclopedia/search.html',{
                "recomendation": recomendation
            })

def create_new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error.html',{
            "msg": "Encyclopedia Already Exist"
        })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html",{
                "title" : title,
                "content" : html_content
            })
        
def edit_entry(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editentry.html",{
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "content" : html_content
        })

def random_entry(request):
    if request.method == "GET":
        entries = util.list_entries()
        random_title = random.choice(entries)
        content = convert_md_to_html(random_title)
        return render(request, 'encyclopedia/entry.html',{
            "title" : random_title,
            "content" : content
        })

'''
from django.shortcuts import render
import markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    return markdown.markdown(content)

def render_entry(request, title, content):
    if content is None:
        return render(request, 'encyclopedia/error.html', {"msg": "Page not found"})
    return render(request, 'encyclopedia/entry.html', {"title": title, "content": content})

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    return render_entry(request, title, convert_md_to_html(title))

def search(request):
    if request.method == "POST":
        search_result = request.POST['q']
        search_content = convert_md_to_html(search_result)
        if search_content is not None:
            return render_entry(request, search_result, search_content)
        else:
            entry_list = util.list_entries()
            recomendation = [entry for entry in entry_list if search_result.lower() in entry.lower()]
            return render(request, 'encyclopedia/search.html', {"recomendation": recomendation})

def create_new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error.html', {"msg": "Encyclopedia Already Exist"})
        util.save_entry(title, content)
        return render_entry(request, title, convert_md_to_html(title))

def edit_entry(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editentry.html", {"title": title, "content": content})

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render_entry(request, title, convert_md_to_html(title))

def random_entry(request):
    if request.method == "GET":
        entries = util.list_entries()
        random_title = random.choice(entries)
        content = convert_md_to_html(random_title)
        return render_entry(request, random_title, content)

'''
