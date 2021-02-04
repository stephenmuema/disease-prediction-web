from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import UserLoginForm
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<hash>[0-9A-Za-z_\-]+)/$',
        views.activate, name='activate'),
    url(r'^profile/$', views.create_profile, name='createprofile'),
    url(r'^forgot/$', views.forgot_password, name='forgot'),
    url(r'^password_update/$', views.password_update, name='password_update'),
    url(r'^password_reset/(?P<hash>[0-9A-Za-z_\-]+)/$',
        views.password_reset, name='password_reset'),
    # url(r'^edit-add_line/$', views.edit_profile, name='panel'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='site/accounts/login.html',
                                     authentication_form=UserLoginForm),
        name='login'),
    url(r'^register/$', views.signup, name='signup'),
    url(r'^add_line/$', views.profile, name='add_line'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^admin/', admin.site.urls),
    # end of authentication for website

]
