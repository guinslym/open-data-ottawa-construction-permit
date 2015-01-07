import urllib2
import os
from bs4 import BeautifulSoup
import urllib
#import requests
#import re
import json

liste_of_data_per_months = []
months = {'Jan':'01','January':'01','Feb':'02','February':'02','Mar':'03','March':'03','Apr':'04',
          'April':'04','May':'05','Jun':'06','June':'06','Jul':'07','July':'07','Aug':'08',
          'August':'08','Sep':'09','September':'09','Oct':'10','October':'10','Nov':'11',
          'November':'11','Dec':'12','December':'12'}

def scrape_given_website(data_url):
    data_page = urllib2.urlopen(data_url)
    soup = BeautifulSoup(data_page, "lxml", from_encoding="UTF-8")
    return soup

def find_all_the_li(soup):
    liste = soup.find(attrs={'class':'resource-list'})
    liste = liste.find_all('li')
    return liste

def populate_dynamicaly_this_list(liste):
    for v in liste:
        liste_of_data_per_months.append(v.a['href'])
        #print v.a['href']


def try_to_rename_the_file(file_name):
    file_name = file_name.split()
    year = file_name[-1]
    month = file_name[0]
    month = months.get(month, month)
    file_name = year + "-" + month
    return file_name

def rename_the_file(soup):
    info = soup.find(attrs={'class':'quick-info'}) 
    file_name = soup.find('dd').string
    file_name = try_to_rename_the_file(file_name)
    file_name =  file_name + ".xls"
    return file_name

def find_the_remote_file_location(soup):
    remote_file_location = soup.table.find_all('td')
    remote_file_location = remote_file_location[-1]
    remote_file_location = remote_file_location.a['href']
    return remote_file_location

def create_a_given_directory():
    if not os.path.exists("open-data-ottawa"):
        os.makedirs("open-data-ottawa")

def download_the_given_file(remote_file_location, local_file_location, file_name):
    local_file_location = "open-data-ottawa/" + file_name
    urllib.urlretrieve (remote_file_location, local_file_location)
    print(file_name)

def body():
    for data in liste_of_data_per_months:
        url = 'http://data.ottawa.ca'
        data_url = url + data
        soup = scrape_given_website(data_url)
        #(return)find the file_name
        file_name =  rename_the_file(soup)
        #print(file_name)
        #(return)remote file
        remote_file_location = find_the_remote_file_location(soup)
        #print(remote_file_location)
        #create the directory
        create_a_given_directory()
        #download the file
        download_the_given_file(remote_file_location, local_file_location, file_name)
        
def main():
    soup = scrape_given_website('http://data.ottawa.ca/dataset/construction-demolition-pool-enclosure-permits-monthly')
    liste = find_all_the_li(soup)
    populate_dynamicaly_this_list(liste)  
    body()


if __name__ == "__main__":