# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import time
from itertools import zip_longest

def get_html(url):
    """Function for get html code from main page"""
    r = requests.get(url)
    return r.text

def get_the_first_page(html):
    """Function for scrape links from main page"""
    links_from_continent = []
    soup = BeautifulSoup(html, 'lxml')
    countries = soup.find('section', class_="directory clearfix col-xs-12").find_all('section')
    for country in countries:
        lin = country.find_all('article')
        for li in lin:
            ads = li.find('ol').find_all('li')
            for ad in ads:
                links = ad.find('div', {'class': 'route-row'}).find('a').get('href')
                links_from_continent.append(links)
    return links_from_continent

def get_html_2(url_2):
    """Function for get html code from other pages of airports"""
    r = requests.get(url_2)
    return r.text

def write_csv(list):
    """Function write csv"""
    with open('therouteshop.csv', 'a') as f:
        writer = csv.writer(f)
        for row in list:
            writer.writerows(zip_longest(*row, fillvalue=''))

def get_the_second_pages(html_2):
    """Function for scrape links from other pages of airports"""
    global email_of_staffs
    global job_titles
    global names_of_staffs
    list = []
    soup = BeautifulSoup(html_2, 'lxml')
    try:
        name_of_airoports = []
        name_of_airoports_1 = soup.find('div', {'class': 'container', 'id': 'main'}) \
            .find('header', {'class': 'col-md-12 col-xs-12 entry-header'}).find('h1', {'class': 'entry-title'}).text.strip()
        name_of_airoports.append(name_of_airoports_1)
        contacts = soup.find('div', {'class': 'container', 'id': 'main'})\
            .find('aside', {'class': 'col-lg-3 col-md-3 col-sm-12 col-xs-12 pull-right profile'})\
            .find('div', {'class': 'profile-meta-wrapper'})\
            .find('div', {'class': 'profile-meta'}).find_all('ul')
        for contact in contacts:
            try:
                names = contact.find_all('li', {'class': 'contact-entry'})
                names_of_staffs = []
                for name in names:
                    names_of_staffs_1 = name.text.strip()
                    names_of_staffs.append(names_of_staffs_1)
            except:
                names = ''
            try:
                emails = contact.find_all('li', {'class': 'contact-entry'})
                email_of_staffs = []
                for email in emails:
                    email_of_staffs_1 = email.find('a').get('href').split(':')[1]
                    email_of_staffs.append(email_of_staffs_1)
            except:
                emails = ''
            try:
                jobs = contact.find_all('li', attrs={'class': None})
                job_titles = []
                for job in jobs:
                    job_1 = job.find_all('strong')
                    for i in job_1:
                        job_titles_1 = i.text.strip()
                        job_titles.append(job_titles_1)
            except:
                jobs = ''
    except:
        contacts = ''
        name_of_airoports = ''
    list.append([name_of_airoports, names_of_staffs, email_of_staffs, job_titles])
    write_csv(list)
    time.sleep(1)

def main():
    url = 'http://www.therouteshop.com/'
    html = get_html(url)
    get_the_first_page(html)
    links_from_continent = get_the_first_page(html) #Links from main page
    for url_2 in links_from_continent:
        html_2 = get_html_2(url_2)
        get_the_second_pages(html_2)

if __name__ == '__main__':
    main()