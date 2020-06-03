from bs4 import BeautifulSoup
import requests

nkw = ''

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR8.TRC0.A0.H0.Xpokemon.TRS2&_nkw='+nkw+'&_sacat=0'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

listings_title = soup.find_all('h3', class_='s-item__title')
listings_link = soup.find_all('a', class_='s-item__link')
listings_price = soup.find_all('span', class_='s-item__price')
listings_shipping = soup.find_all('span', class_='s-item__shipping s-item__logisticsCost')


item_title = []
item_price = []
item_link = []
item_shipping = []


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


master_list = zip(item_title, item_price, item_shipping,)
super_list = [list(a) for a in master_list]









