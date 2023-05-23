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
from utils.plaid_client import create_client
from django.http import HttpResponse
import plaid






from django.db.models import Sum
from .models import Expense, Budget, FinancialGoal, Transaction
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


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
    user = form.save(commit=False)
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

        # Authenticate user
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
    # Calculate total expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch budgets
    budgets = Budget.objects.filter(user=request.user)

    # Calculate remaining budget
    remaining_budget = (budgets.aggregate(Sum('amount'))['amount__sum'] or 0) - total_expenses

    # Fetch saving goals
    saving_goals = FinancialGoal.objects.filter(user=request.user)

    # Calculate progress towards saving goals
    total_saving_goals = saving_goals.aggregate(Sum('goal_amount'))['goal_amount__sum'] or 0
    achieved_saving_goals = saving_goals.filter(achieved=True).aggregate(Sum('goal_amount'))['goal_amount__sum'] or 0
    progress_percentage = (achieved_saving_goals / total_saving_goals) * 100 if total_saving_goals else 0

    # Calculate savings goal range
    savings_goal_range = saving_goals.aggregate(Sum('goal_amount'))['goal_amount__sum'] * 0.5 if total_saving_goals else 0

    # Generate expense category pie chart
    expense_categories = Expense.objects.filter(user=request.user).values('category').annotate(total_amount=Sum('amount'))
    categories = [category['category'] for category in expense_categories]
    amounts = [category['total_amount'] for category in expense_categories]
    fig = px.pie(names=categories, values=amounts, title='Expense Categories')

    # Generate monthly expense line chart
    monthly_expenses = Expense.objects.filter(user=request.user).extra(select={'month': 'strftime("%%m", date)'}).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    months = [expense['month'] for expense in monthly_expenses]
    amounts = [expense['total_amount'] for expense in monthly_expenses]
    df = pd.DataFrame({'Month': months, 'Total Amount': amounts})
    fig2 = px.line(df, x='Month', y='Total Amount', title='Monthly Expenses')

    context = {
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'saving_goals': saving_goals,
        'progress_percentage': progress_percentage,
        'savings_goal_range': savings_goal_range,
        'expense_chart': fig.to_html(full_html=False, default_height=400),
        'monthly_expense_chart': fig2.to_html(full_html=False, default_height=400),
    }
    return render(request, 'dashboard.html', context)



def get_bank_accounts(request):
    plaid_client = create_client()

    # Example: Retrieve bank accounts
    access_token = 'access_token_from_plaid_link'
    accounts_response = plaid_client.Accounts.get(access_token)
    accounts = accounts_response['accounts']

    # Process the accounts or return them in the response

    return HttpResponse('Bank accounts retrieved successfully')

def add_bank(request):
    # Generate Plaid Link token
    client = plaid.Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, environment=settings.PLAID_ENV)
    token_response = client.LinkToken.create(
        {
            'user': {
                'client_user_id': request.user.id,
            },
            'client_name': 'Personal Finance Manager',
            'products': ['auth', 'transactions'],
            'country_codes': ['US'],
            'language': 'en',
        }
    )
    link_token = token_response['link_token']

    context = {'link_token': link_token}
    return render(request, 'add_bank.html', context)


