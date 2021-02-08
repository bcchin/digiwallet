from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *



# Handles User Registriation, Login, and Logout pages
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = UserCreationForm()
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			
		context = {'form':form}
		return render(request, 'registration/sign_up.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'registration/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


# Handles main page (dashboard expenses page)
# Only Displays data from database that was created by the current user
@login_required(login_url='login')
def dashboard(request):
	if request.method == 'POST':
		expense_form = ExpenseForm(request.POST or None)
		if expense_form.is_valid():
			expense = expense_form.save(commit=False)
			expense.user = request.user
			expense.save()

	# Calculates the user's current balance based on transactions, rounded to two decimal places
	balance = ExpenseInfo.objects.filter(user=request.user).aggregate(balance=Sum('amount'))
	expenses = ExpenseInfo.objects.filter(user=request.user).aggregate(expenses=Sum('amount',filter=Q(amount__lt=0)))
	income = ExpenseInfo.objects.filter(user=request.user).aggregate(income=Sum('amount',filter=Q(amount__gt=0)))

	if (balance['balance'] is not None):
		balance['balance'] = '{:0.2f}'.format(balance['balance'])
	else:
		balance['balance'] = '0.00'
	if (expenses['expenses'] is not None):
		expenses['expenses'] = '{:0.2f}'.format(abs(expenses['expenses']))
	else:
		expenses['expenses'] = '0.00'
	if (income['income'] is not None):
		income['income'] = '{:0.2f}'.format(income['income'])
	else:
		income['income'] = '0.00'

	context ={'transactions':ExpenseInfo.objects.filter(user=request.user),'balance':balance['balance'],'expenses':expenses['expenses'], 'income':income['income']}
	return render(request,'dashboard.html', context)

# Deletes selected transaction and updates dashboard page
@login_required(login_url='login')
def delete(request, transaction_id):
    item = ExpenseInfo.objects.get(pk=transaction_id)
    item.delete()
    return redirect('dashboard')