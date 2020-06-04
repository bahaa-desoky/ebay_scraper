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
        item_shipping_calc = []
        item_condition = []
        total_price = []

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
            no_symbols = text_only.replace('+', '').replace('Shipping', '').replace('shipping', '').\
                replace('Free', '0').replace('International', '').replace(' ', '')
            item_shipping.append(no_plus)
            item_shipping_calc.append(no_symbols)

        for listing in listings_condition:
            text_only = listing.text
            item_condition.append(text_only)

        for i1, i2 in zip(item_price, item_shipping_calc):
            i1, i2 = i1.replace('$', ' '), i2.replace('$', ' ')
            items = i1.split('-')
            added_items = [str(round(float(item) + float(i2), 2)) for item in items]
            total_price.append('-'.join(added_items))

        total_price = ['$' + s for s in total_price]

        master_list = zip(item_title, item_condition, item_price, item_shipping, total_price)
        super_list = [list(a) for a in master_list]

        context = {
            'items': super_list,
        }
        return render(request, 'scraper/home.html', context)
    return render(request, 'scraper/home.html')
