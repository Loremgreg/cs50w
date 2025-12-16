from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
from django.http import Http404
import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
# La def doit :
# 	1.	Recevoir le nom recherché
# 	2.	Vérifier si le fichier existe
# 	3.	Lire le contenu du fichier .md
# 	4.	L’envoyer au template    
    # On récupère le contenu de l'entrée en utilisant le titre fourni dans l'URL
    content = util.get_entry(title)

    # Cas 1 : L'entrée n'existe pas
    if content is None:
            raise Http404(f"{title} does not exist")
    
    # Cas 2 : L'entrée existe
    else:
        # On convertit le contenu Markdown en HTML
        content = markdown2.markdown(content)
        # On affiche la page de l'entrée avec son titre et son contenu
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
        })

def search(request):
    """
    Search view:
    - reads query from request.GET['q']
    - if query empty -> redirect to index
    - if exact match (case-insensitive) -> redirect to that entry page
    - otherwise -> render search results (entries containing query, case-insensitive)
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return redirect("index")

    entries = util.list_entries()

    # exact match (case-insensitive)
    for entry in entries:
        if entry.lower() == q.lower():
            return redirect("entry", title=entry)

    # partial matches (case-insensitive)
    results = [entry for entry in entries if q.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": q,
        "results": results
    })

def new_page(request):
     if request.method == "POST":
        # Récupérer les données : title et content
          title = request.POST.get("title", "").strip()
          content = request.POST.get("content", "").strip()


          # Validation basique
          if not title:
               return render(request, "encyclopedia/new.html", {
                "error": "Title is required.",
                "title": title,
                "content": content
            })

        # Vérifier doublon (insensible à la casse) avec  util.list_entries() 
          entries = util.list_entries()
          for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/new.html", {
                    "error": "An entry with this title already exists.",
                    "title": title,
                    "content": content
                })

        # Sauvegarder et rediriger vers la nouvelle page avec util.save_entry
          util.save_entry(title, content)
          return redirect("entry", title=title)

    # GET -> afficher le formulaire vide
     elif request.method == "GET":
          return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    """
    Edit view:
    - GET: render form pre-filled with existing markdown content
    - POST: save updated content and redirect to the entry page
    """
    content = util.get_entry(title)
    if content is None:
        raise Http404(f"{title} does not exist")

    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        util.save_entry(title, new_content)
        return redirect("entry", title=title)

    # GET
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })