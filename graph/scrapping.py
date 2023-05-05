# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def scrapping(name, model, year):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    url = 'https://www.cars.com/research/'+name+'-'+model+'-'+str(year)+'/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            car = {}
            car_name = soup.find(
                "h1", {"class": "sds-heading--1 sds-page-section__title"}).get_text().strip()
            car_year = car_name.split(' ')[0]
            car_marque = car_name.split(' ')[1]
            car_model = car_name.split(' ')[2]
            car_mpg = soup.find_all(
                "p", {"class": "key-specs-text"})[1].get_text().split(' ')[0]
            car_seats = soup.find_all(
                "p", {"class": "key-specs-text"})[2].get_text().split(' ')[0]
            car_pros = soup.find_all(
                "ul", {"class": "sds-list sds-list--unordered pros-cons-list"})[0].get_text().strip()
            car_cons = soup.find_all(
                "ul", {"class": "sds-list sds-list--unordered pros-cons-list"})[1].get_text().strip()
            car['car_name'] = car_name
            car['car_year'] = car_year
            car['car_marque'] = car_marque
            car['car_model'] = car_model
            car['car_mpg'] = car_mpg
            car['car_seats'] = car_seats
            car['car_desc'] = '----Pros----\n' + \
                car_pros+'\n----Cons----\n'+car_cons
            return car
        else:
            return "Unknown Car"

    except:
        return "URL Error"
