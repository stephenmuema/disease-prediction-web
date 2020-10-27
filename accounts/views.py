from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import SignUpForm, ForgotPasswordForm, ProfileForm, ProfileAccountForm, NewPasswordForm
from accounts.models import User
from djangoHealthAnalytics.extras import split_domain_ports
from pages.models import Images
from .tokens import account_activation_token


# @login_required(login_url='site/accounts:login')
# def panel(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('%s?next=%s' % ('site/accounts:login', request.path))
#     user = User.objects.get(pk=request.user.pk)
#     if user.user_type == "customer":
#         if user.email_confirmed:
#             return redirect('index')
#         else:
#             return HttpResponse("<p>Please verify your account using the link sent to your email address</p>")
#
#     elif user.user_type == "staff":
#         return redirect('staff:panel')
#     elif user.user_type == 'seller':
#         return redirect('sellers:panel')
#     elif user.user_type == "admin":
#         return redirect('/michpastries-admin/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('site/accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                'info@' + split_domain_ports(request.get_host()),
                [user.email],
                fail_silently=False,
            )

            return redirect('accounts:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'site/accounts/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'site/accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('accounts:panel')
    else:
        return render(request, 'site/accounts/account_activation_invalid.html')


def resettoken(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('accounts:panel')
    else:
        return render(request, 'site/accounts/account_activation_invalid.html')


@login_required(login_url='accounts:login')
def logout_view(request):
    Images.objects.filter(user=User.objects.get(pk=request.user.pk)).delete()
    logout(request)

    return redirect('accounts:login')


def edit_profile(request):
    return None


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        print(form.errors)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data.get("email"))

                current_site = get_current_site(request)
                subject = 'Password Request Link'
                message = render_to_string('site/accounts/password_reset.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(
                    subject,
                    message,
                    'info@' + split_domain_ports(request.get_host()),
                    [user.email],
                    fail_silently=False,
                )
                print("sent email")
                return render(request, 'site/accounts/reset-email-sent.html')
            except:
                print("user does not exist")
                messages.error(request, 'such an account does not exist')
                return redirect("accounts:forgot")


        else:
            print("did not send email due to invalid form")
            form = ForgotPasswordForm()
            return render(request, 'site/accounts/forgot.html', {'form': form})

    else:
        print("did not send email..just loaded the page")
        form = ForgotPasswordForm()
        return render(request, 'site/accounts/forgot.html', {'form': form})


def profile(request):
    return redirect('accounts:panel')


@login_required(login_url='accounts:login')
def create_profile(request):
    user = User.objects.get(pk=request.user.pk)
    signupform = ProfileAccountForm(
        initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})

    if profile:
        print("profile ala")
        profile_form = ProfileForm(
            initial={'address': user.profile.address,
                     'mobile_money_phone_number': user.profile.mobile_money_phone_number,
                     'alternative_phone_number': user.profile.alternative_phone_number,
                     'location': user.profile.location}
        )
    else:
        profile_form = ProfileForm()

    if request.method == 'POST':
        signupform = ProfileAccountForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if profile_form.is_valid() and signupform.is_valid():
            signupform.save()
            obj = profile_form.save(commit=False)
            obj.save()
        else:
            print(profile_form.errors)
    context = {'cart_count': 0, 'form_profile': profile_form, 'form_signup': signupform, 'user': user}

    return render(request, 'site/accounts/profile.html', context)


def password_reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        form = NewPasswordForm()
        return render(request, 'site/accounts/password_reset_form.html', {'user': user, 'form': form})
    else:
        return render(request, 'site/accounts/account_activation_invalid.html')


def password_update(request):
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        print(form.errors)
        if form.is_valid():
            try:
                user = User.objects.get(hash=request.POST.get('user'))
                password = form.cleaned_data['password2']
                user.set_password(password)
                user.save()
                return redirect('accounts:login')
            except:
                print("user does not exist")
                messages.error(request, 'such an account does not exist')
                return redirect("accounts:forgot")


        else:
            print("did not send email due to invalid form")
            form = NewPasswordForm()
            return render(request, 'site/accounts/forgot.html', {'form': form})

    else:
        form = NewPasswordForm()
        return render(request, 'site/accounts/forgot.html', {'form': form})
