from django.shortcuts import render
from . import scraper_code

# Create your views here.

items = {
    'main': scraper_code.super_list,
    'links': scraper_code.item_link,
    'title': scraper_code.item_title,
    'price': scraper_code.item_price,
}


def home(request):
    context = {
        'items': items,
    }
    return render(request, 'scraper/home.html', context)
