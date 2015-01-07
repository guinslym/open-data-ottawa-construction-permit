# open-data-ottawa-construction-permit


###description
This module ease the download of all the file of any data set from [open-data-ottawa](http://data.ottawa.ca/en). This package works only for python2 ...(for now)

## Usage ##
		
		python ct.py #this will download all the file of the permit construction dataset

## Usage import ##

		import ct
		construction = Permit()
		construction.download_all_the_necessary_file('http://data.ottawa.ca/dataset/construction-demolition-pool-enclosure-permits-monthly')


###todo
* python3 support
* create a pakage for pypi
* replace urllib to requests
* pytest :)


