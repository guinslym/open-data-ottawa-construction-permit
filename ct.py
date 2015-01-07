#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import urllib2
import os
from bs4 import BeautifulSoup
import urllib
import time
#import requests
#import re
import json

class Permit:
  """A simple example class to download all the excel file (open data) from
  http://data.ottawa.ca/dataset/construction-demolition-pool-enclosure-permits-monthly
  to set up doing some data analytic in ipython
  """

  LISTE_OF_DATA_PER_MONTHS = []
  MONTHS = {'Jan':'01','January':'01','Feb':'02','February':'02','Mar':'03','March':'03','Apr':'04','April':'04','May':'05','Jun':'06','June':'06','Jul':'07','July':'07','Aug':'08','August':'08','Sep':'09','September':'09','Oct':'10','October':'10','Nov':'11','November':'11','Dec':'12','December':'12'}
  
  
  def scrape_given_website(self,data_url):
      data_page = urllib2.urlopen(data_url)
      soup = BeautifulSoup(data_page, "lxml", from_encoding="UTF-8")
      return soup

  def find_all_the_li(self, soup):
      liste = soup.find(attrs={'class':'resource-list'})
      liste = liste.find_all('li')
      return liste

  def populate_dynamicaly_this_list(self, liste):
      if len(self.LISTE_OF_DATA_PER_MONTHS) > 0:
      	  self.LISTE_OF_DATA_PER_MONTHS = []
      for v in liste:
          self.LISTE_OF_DATA_PER_MONTHS.append(v.a['href'])
          #print v.a['href']

  def try_to_rename_the_file(self, file_name):
      if ' ' not in file_name:
          return file_name
      file_name = file_name.split()
      #print(file_name)
      year = file_name[-1]
      month = file_name[0]
      month = self.MONTHS.get(month, month)
      file_name = year + "-" + month
      return file_name

  def rename_the_file(self, soup):
      info = soup.find(attrs={'class':'quick-info'}) 
      file_dl = soup.find('dl')
      file_all_dd = file_dl.find_all('dd')
      file_name = file_all_dd[0].string
      #print(file_name)
      file_extension = file_all_dd[2].string
      file_extension =file_extension.strip()
      #print(file_extension)
      file_name = self.try_to_rename_the_file(file_name)
      #need to find the format file
      file_name =  file_name + "."+ file_extension
      return file_name

  def find_the_remote_file_location(self,soup):
      remote_file_location = soup.table.find_all('td')
      remote_file_location = remote_file_location[-1]
      remote_file_location = remote_file_location.a['href']
      return remote_file_location

  def create_a_given_directory(self):
      if not os.path.exists("open-data-ottawa"):
          os.makedirs("open-data-ottawa")

  def download_the_given_file(self, remote_file_location, file_name):
      local_file_location = "open-data-ottawa/" + file_name
      urllib.urlretrieve (remote_file_location, local_file_location)
      print(file_name)

  def body(self):
      for data in self.LISTE_OF_DATA_PER_MONTHS:
          url = 'http://data.ottawa.ca'
          data_url = url + data
          soup = self.scrape_given_website(data_url)
          file_name =  self.rename_the_file(soup)
          remote_file_location = self.find_the_remote_file_location(soup)
          self.create_a_given_directory()
          self.download_the_given_file(remote_file_location,  file_name)
      
  def download_all_the_necessary_file(self, url):
      soup = self.scrape_given_website(url)
      title = soup.find('h1').string
      #TITLE ....for some webpage there is a strange error
      "ascii' codec can't encode character u'\u2013' in position 9: ordinal not in range(128)"
      liste = self.find_all_the_li(soup)
      self.populate_dynamicaly_this_list(liste) 
      print('we will start downloading all {0} file from this dataset {1} '.format(len(self.LISTE_OF_DATA_PER_MONTHS), title)) 
      self.body()


if __name__ == "__main__":
    construction = Permit()
    construction.download_all_the_necessary_file('http://data.ottawa.ca/dataset/construction-demolition-pool-enclosure-permits-monthly')

'''
Function that I would like to add
import ct
#print(dataset = ct.list_of_dataset)
#or dataset = ct.find_this_dataset('construction')
#or ct.print_the_url_of('construction')
ct.download_all_the_necessary_file(dataset_url)
'''
