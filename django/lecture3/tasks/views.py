from django.shortcuts import render

tasks = ["foo", "bar", "baz"]

# Create your views here.
def index(request):
    return render(request, "tasks/index.html", {
        "tasks": tasks
    })

# Add a new task:
def add(request):
    return render(request, "tasks/add.html")