from pathlib import Path

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    #if (content := util.get_entry(title)):

    #else:
        # Error message "Page not found"
        
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title),
    })
