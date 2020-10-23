from django.urls import path
from rest_framework.authtoken import views as tv

from . import views

app_name = 'api'
urlpatterns = [
    # end of authentication for website
    path('token/', tv.obtain_auth_token, name='token_obtain'),
    path('files/', views.FileList.as_view(), name='files'),

]
