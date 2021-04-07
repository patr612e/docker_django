from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Costumer, Account, Ledger
from .forms import CostumerForm, AddCostumer

# Create your views here

@login_required
def index(request):

    costumer_form = AddCostumer()
    users = User.objects.all()
    all_accounts = Account.objects.all()
    accounts = Account.objects.filter(user=request.user, is_account=True)
    loans = Account.objects.filter(user=request.user, is_account=False)

    # get costumer of logged in user, pass it to template
    costumer = Costumer.objects.get(user=request.user)

    context = {
        'accounts': accounts,
        'loans': loans,
        'all_accounts': all_accounts,
        'users': users,
        'costumer': costumer,
        'costumer_form': costumer_form,
    }

    return render(request, 'bank_app/index.html', context)


def add_user(request):
    #try:

        if request.method == "POST":
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone']
            rank = request.POST['rank']

            # doesnt work
            def is_employee(request):
                if request.POST.get('is_employee'):
                    return True
                else:
                    return False
            
            user = User.objects.create_user(username, email, password)

            if user:

                user.first_name = firstname
                user.last_name = lastname
                user.save()

                costumer = Costumer()

                costumer.user = user
                costumer.phone = phone
                costumer.is_employee = is_employee(request)
                costumer.save()

        return HttpResponseRedirect(reverse('bank_app:index'))
    
    #except:
        #return HttpResponse('<h1>Username has already been used - try again</h1>')


def change_rank(request):

    pk = request.POST['pk']
    rank = request.POST['rank']
    user = User.objects.get(pk=pk)
    costumer = Costumer.objects.get(user=user)
    costumer.rank = rank
    costumer.save()

    return HttpResponseRedirect(reverse('bank_app:index'))


def add_account(request):
    pk = request.POST['pk']
    account_name = request.POST['account']
    user = User.objects.get(pk=pk)
    account = Account(user=user, name=account_name)
    account.save()

    return HttpResponseRedirect(reverse('bank_app:index'))


def transfer_money(request):

    credit_id = request.POST['from_account']
    debit_id = request.POST['to_account']
    amount = request.POST['amount']
    text = request.POST['text']

# check if debit_id exists

    if Account.objects.filter(id=debit_id).exists():

        if Account.objects.get(user=request.user, id=credit_id).balance >= int(amount):

            Ledger.transaction(amount, text, debit_id, credit_id)
            return HttpResponseRedirect(reverse('bank_app:index'))

        else:
            return HttpResponse("<h1>Sorry, insufficient funds</h1>")

    else:
        return HttpResponse("<h1>Sorry, receiver account doesn't exist</h1>")



def make_loan(request):

    amount = request.POST['amount']
    text = request.POST['text']
    loan_name = request.POST['loan_name']

    # get id of debit account
    account_id = request.POST['account_name']

    account = Account(user=request.user, name=loan_name, is_account=False)
    account.save()
    
    # get id of credit account
    loan_id = account.id

    # if the given account name exists and belongs to the user

    if Account.objects.filter(user=request.user, id=account_id).exists():
        Ledger.transaction(amount, text, account_id, loan_id)

    return HttpResponseRedirect(reverse('bank_app:index'))



def account_detail(request, Costumer_id): 

    try:
        user = User.objects.get(id=Costumer_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")


    costumer = Costumer.objects.get(user=request.user)
    accounts = Account.objects.filter(user=user)

    # ledgers must be account instance

    ledgers = Ledger.objects.filter(account__in=accounts).order_by('-timestamp')

    

    context = {
        'user' : user,
        'accounts' : accounts, 
        'ledgers' : ledgers
    }

    if costumer.is_employee or Costumer_id == request.user.id:
        return render(request, 'bank_app/account_detail.html', context)
    else:
        raise Http404("not employee")


    
    

