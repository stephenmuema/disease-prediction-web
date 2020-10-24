from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import User
from pages.forms import SearchForm
from pages.ml import ML


def index(request):
    return redirect('accounts:login')


def contact(request):
    return None


def about(request):
    return None

@login_required
def panel(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            user=User.objects.get(pk=request.user.pk)
            disease = form.cleaned_data['disease_name'].lower()

            location = form.cleaned_data['location'].lower()
            ml = ML(disease=disease, location=location)
            ml.generate_csv()
            ml.generate_predictions(user.email)
        else:
            print("invalid form")
    else:
        form = SearchForm()

    return render(request, 'site/panel.html', {'form': form})
