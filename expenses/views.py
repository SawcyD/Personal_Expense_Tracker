from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from django.db.models import Sum
from .models import Expense


from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			return register_user_inactive(form, request)
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})


# TODO Rename this here and in `register` Django view to `register_user_inactive`
def register_user_inactive(form, request):
	user = form.save(commit = False)
	user.is_active = False
	user.save()


	current_site = get_current_site(request)
	subject = 'Activate Your Account'
	mail_subject = 'Activate your account.'
	message = render_to_string('verification_email.html', {
		'user': user,
		'domain': current_site.domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': default_token_generator.make_token(user),

	})
	send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

	return redirect('verification_sent')

def verification_sent(request):
	return render(request, 'verification_sent.html')

def verify_email(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk = uid)
		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			return redirect('login')
		else:
			return render(request, 'verification_failed.html')
	except User.DoesNotExist:
		return render(request, 'verification_failed.html')
def login_view(request):
	# sourcery skip: inline-variable, last-if-guard, remove-unnecessary-else, swap-if-else-branches
	"""

	:param request:  Request object
	:return:  Redirect to dashboard if user is authenticated, else render login page
	"""
	if request.method == 'POST':
		username = request.POST.get ('username')
		password = request.POST.get ('password')

		# Authenticate user TODO: Use Django's built-in authentication
		user = authenticate (username = username, password = password)

		if user is not None:
			# valid Credentials, log in
			login (request, user)
			return redirect ('dashboard')
		else:
			# invalid credentials
			error_message = 'Invalid Credentials'
			return render (request, 'login.html', {'error_message': error_message})

	else:
		return render (request, 'login.html')


def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('dashboard')
@login_required(login_url='login')
def dashboard(request):


	total_expenses = Expense.objects.filter(user_id=request.user).aggregate(Sum('amount'))['amount__sum']

	context = {
		'total_expenses': total_expenses
	}
	return render(request, 'dashboard.html', context)