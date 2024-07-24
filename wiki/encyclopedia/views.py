from pathlib import Path
import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # If entry not found, show error
    if not (entry := util.get_entry(title)):
        title = "Error"
        entry = "Error: Page not found."
    # Otherwise show entry's markdown contents
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(entry),
    })

def search(request):
    query = request.GET.get("q")
    # If there is an entry that matches that title
    if query in util.list_entries():
        entry = util.get_entry(query)
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": markdown2.markdown(entry)
        })
    else:
        # List for pages with matching substring
        matches = []
        # Check each entry for presence of substring
        for title in util.list_entries():
            if query in markdown2.markdown(util.get_entry(title)):
                matches.append(title)
        return render(request, "encyclopedia/search.html", {
            "matches": matches
        })
