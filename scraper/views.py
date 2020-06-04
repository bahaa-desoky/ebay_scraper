from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup

# Create your views here.


def home(request):

    if request.method == 'POST':
        item_title = []
        item_price = []
        item_link = []
        item_shipping = []
        item_condition = []

        nkw = request.POST['nkw']
        url = 'https://www.ebay.com/sch/' + nkw

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        listings_title = soup.find_all('h3', class_='s-item__title')
        listings_link = soup.find_all('a', class_='s-item__link')
        listings_price = soup.find_all('span', class_='s-item__price')
        listings_shipping = soup.find_all('span', class_='s-item__shipping s-item__logisticsCost')
        listings_condition = soup.find_all('span', class_='SECONDARY_INFO')


        for listing in listings_title:
            text_only = listing.text
            no_newListing = text_only.replace('New Listing', '').replace('Ã—', '×')
            item_title.append(no_newListing)

        for listing in listings_price:
            text_only = listing.text
            no_dash = text_only.replace(' to ', '-')
            item_price.append(no_dash)

        for listing in listings_link:
            item_link.append(listing['href'])

        for listing in listings_shipping:
            text_only = listing.text
            no_plus = text_only.replace('+', '').replace('Shipping', '').replace('shipping', '')
            item_shipping.append(no_plus)

        for listing in listings_condition:
            text_only = listing.text
            item_condition.append(text_only)

        master_list = zip(item_title, item_price, item_shipping, item_condition, item_link)
        super_list = [list(a) for a in master_list]

        context = {
            'items': super_list,
        }
        return render(request, 'scraper/home.html', context)
    return render(request, 'scraper/home.html')
