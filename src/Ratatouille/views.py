from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(request, "Ratatouille/index.html", context={"date": datetime.today()})