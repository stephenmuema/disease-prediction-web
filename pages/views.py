from django.shortcuts import render, redirect

# Create your views here.
from pages.forms import SearchForm


def index(request):
    return redirect('accounts:login')


def contact(request):
    return None


def about(request):
    return None


def panel(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
    else:
        form = SearchForm()

    return render(request, 'site/panel.html', {'form': form})
