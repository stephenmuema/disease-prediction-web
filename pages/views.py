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

import io # use import io in Python 3x
import base64

# def generate_image():
#     if request.method == 'POST':
#         x_coord = request.POST['x-coordinate']
#         y_coord = request.POST['y-coordinate']
#
#         # generate a matplotlib image, (I don't know how to do that)
#
#         sio = io.StringIO() # use io.StringIO() in Python 3x
#         pyplot.savefig(sio, format="PNG")
#
#         encoded_img = sio.getvalue().encode('Base64') # On Python 3x, use base64.b64encode(sio.getvalue())
#
#         return HttpResponse('<img src="data:image/png;base64,%s" />' %encoded_img)
#     else:
        # Do something ...
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
