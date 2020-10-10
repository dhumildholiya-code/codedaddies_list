import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup

from .models import Search

BASE_CRAIGLIST_URL = 'https://ahmedabad.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = "N/A"
        if post.find(class_='result_price'):
            post_price = post.find(class_='result_price').text
        post_image_url = 'https://craigslist.org/images/peace.jpg'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)

        final_postings.append((post_title, post_url, post_price, post_image_url))

    context = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', context)
