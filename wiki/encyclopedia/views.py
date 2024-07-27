import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"name":"title"}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"name":"content", "rows":"5"}), label="Markdown")


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


def newpage(request):
    # Submit new page form
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })
            else:
                # Save new page entry
                util.save_entry(title, content)
                # Redirect to the new page
                return redirect("encyclopedia:entry", title=title)
                #return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
            })
    # Show new page form
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm(),
    })