from django.shortcuts import render
import markdown
from . import util

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
        return render(request, 'encyclopedia/error.html')
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
    return render(request, "encyclopedia/createpage.html")

