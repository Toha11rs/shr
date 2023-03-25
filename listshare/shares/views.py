from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from listshare.forms import BuyShareForm, AddFundsForm
from shares.models import Share, Transaction, Portfolio, Balance
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
import requests
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages


def pay(request):

    return render(request, 'registration/share/pay.html')


def get_stock_data(symbol):
    api_key = 'P0Q18U8ZUO33ZZ7R'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()['Time Series (Daily)']
    stock_data = []
    for date in data:
        stock_data.append({
            'date': date,
            'open': float(data[date]['1. open']),
            'high': float(data[date]['2. high']),
            'low': float(data[date]['3. low']),
            'close': float(data[date]['4. close']),
            'volume': int(data[date]['6. volume'])
        })
    return stock_data


def logout_view(request):
    logout(request)
    return redirect('login')


def user(request):

    return render(request, 'registration/share/user.html')


def buy_share_view(request):
    balance = Balance.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user
        share_ticker = request.POST.get('share_ticker')
        share_quantity = int(request.POST.get('share_quantity'))
        share_price = float(request.POST.get('share_price'))
        share = Share.objects.get(ticker=share_ticker)
        balance = Balance.objects.get(user=user)
        total_price = share_price * share_quantity
        if balance.amount >= total_price:
            balance.amount -= total_price
            balance.save()
            portfolio, created = Portfolio.objects.get_or_create(
                user=user, share=share)
            if not created:

                portfolio.quantity += share_quantity
                portfolio.save()
            else:

                portfolio.quantity = share_quantity
                portfolio.purchase_price = share_price
                portfolio.save()
            transaction = Transaction.objects.create(
                user=user,
                share=share,
                quantity=share_quantity,
                price=share_price,

                is_buy=True
            )
            return redirect('index')
        else:
            context = {
                'error': 'недостаточно средств',
                'shares': Share.objects.all()
            }
            return render(request, 'registration/share/b_share.html', context)
    else:
        context = {
            'shares': Share.objects.all(),
            'balance': balance.amount,
        }
        return render(request, 'registration/share/b_share.html', context)


def stock_chart(request, symbol):

    stock_data = get_stock_data(symbol)
    balance = Balance.objects.get(user=request.user)
    context = {'balance': balance.amount,
               'stock_data': stock_data, "tik": symbol}
    return render(request, 'registration/share/stock_chart.html', context)


def index(request):
    resultsdisplay = Share.objects.all()
    balance = Balance.objects.get(user=request.user)
    context = {'balance': balance.amount, "shares": resultsdisplay}
    return render(request, 'registration/share/index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def portfolio_view(request):

    user = User.objects.get(pk=request.user.id)

    holdings = Portfolio.objects.filter(user=user)

    for holding in holdings:
        holding.current_price = Share.objects.get(
            ticker=holding.share.ticker).price
        holding.price_change = (
            holding.current_price - holding.purchase_price) / holding.purchase_price * 100
        holding.return_on_investment = (
            holding.current_price / holding.purchase_price - 1) * 100

    balance = Balance.objects.get(user=request.user)

    return render(request, 'registration/share/buy_share.html', {'user': user, 'holdings': holdings, 'balance': balance.amount, })


def add_funds_view(request):
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            balance, _ = Balance.objects.get_or_create(user=request.user)
            balance.amount += amount
            balance.save()
            messages.success(
                request, f'Your balance has been updated. Current balance is {balance.amount}')
            return redirect('index')
    else:
        form = AddFundsForm()
    return render(request, 'registration/share/pay.html', {'form': form})
