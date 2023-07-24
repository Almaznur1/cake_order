from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, Cake, Topping, Berry, Decor, CakeLevel, CakeForm, OrderCake

import io
import base64


# Create your views here.
def index(request):

    return HttpResponse(f'<h1>СОБРАТЬ СВОЙ АВТОРСКИЙ ТОРТ!</h1> '\
        # f'<img src="../pictures/Tort.png" >'
        # f'Client: {Client.get_client("234")}'\
        # f'<p>{record1}</p>'
        )