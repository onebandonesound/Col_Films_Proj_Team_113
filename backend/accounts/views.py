from django.shortcuts import  render, redirect
from .forms import NewUserForm, SignUpForm, UserForm
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from . models import CustomUser
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from .decorators import ajax_required
from .tokens import account_activation_token


def homepage(request):
	User = CustomUser.objects.all() #queryset containing all books we just created
	return render(request=request, template_name="main/home.html", context={'user':User})


def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # User shouldn't log in before confirming email
            user.is_active = False
            user.save()
            # Load profile instance created by the signal
            user.refresh_from_db()
            user.profile.favorite_club = form.cleaned_data.get('favorite_club')
            user.save()
            current_site = get_current_site(request)

            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            
            subject = render_to_string(
                'registration/account_activation_subject.txt', 
                {'site_name': current_site.name}
            )
            
            message = render_to_string(
                'registration/account_activation_email.html',
                {'user': user,
                 'domain': current_site.domain,
                 'protocol': protocol,
                 'site_name': current_site.name,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),}
            )
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            messages.error(request, "An error occured while trying to create your account.")
            return render(request,
                'registration/signup.html',
                {'form': form})
    else:
        form = SignUpForm()

    template = 'registration/signup.html'
    context = {
        'form': form
    }
    
    return render(request, template, context)


def account_activation_sent(request):
    if request.user.is_authenticated():
        return redirect('home')

    template = 'registration/account_activation_sent.html'
    context = {}

    return render(request, template, context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Your profile has been successully created.')
        return redirect('home')
    else:
        return render(
            request,
            'registration/activate.html',
            {})
  