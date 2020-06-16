import requests
import re
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models


def home(request) :
    return render(request , 'base.html')



def New_Search(request) :
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    url = "https://bangalore.craigslist.org/search/hhh?query={}&min_price={}&max_price={}"
    min_price = request.POST.get('min_price' , 0)
    max_price = request.POST.get('max_price' , 1000000000)
    main_url = url.format(quote_plus(search), min_price, max_price)
    response = requests.get(main_url)
    data = response.text
    soup = BeautifulSoup(data , 'html.parser')
    post_listings = soup.findAll('li' , {'class' : 'result-row'})
    final_posting = []
    for post in post_listings :
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else :
            new_response = requests.get(post_url)
            new_data = new_response.text
            new_BS = BeautifulSoup(new_data , 'html.parser')
            post_text = new_BS.find(id='postingbody').text
            r1 = re.findall(r'\$\w+' , post_text)
            if r1:
                post_price = r1[0]
            else :
                post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids') :
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
        else :
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((post_title , post_url , post_price , post_image_url))

    frontend = dict(search=search , final_posting=final_posting)

    return render(request, 'my_app/new_search.html', frontend)
