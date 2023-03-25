"""listshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path
from shares.views import login_view, pay, index, user, portfolio_view, stock_chart, buy_share_view, add_funds_view, Register

# login_view, logout_view, register_view, buy_share_view, sell_share_view

urlpatterns = [
    # path('', home_view, name='home'),
    path("pay/", add_funds_view, name='pay'),
    path("index", index, name='index'),
    path("user", user, name='user'),
    path('', login_view, name='login'),
    path('register/', Register.as_view(), name='register'),
    path('stock/<str:symbol>/', stock_chart, name='stock_chart'),
    #path('logout/', logout_view, name='logout'),
    path('buy_share/', portfolio_view, name='buy_share'),
    path('sell_share/', buy_share_view, name='sell_share'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
