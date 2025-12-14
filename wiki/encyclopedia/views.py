from django.shortcuts import render
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

