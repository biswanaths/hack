#!/usr/bin/env python

'''

@Author : Biswanath 
@Date   : 29th Aug, 2015

'''
import urllib2
import hashlib
import re
from bs4 import BeautifulSoup
import secrets



'''
base id 27454 - 1
end  id 27543 - 100
Don't use this any more
'''
def create_base():
    for i in range(1,101):
        url=create_format.format(str(i))
        urllib2.urlopen(url)
        print "created {0}".format(i)

def main():
    print "do not use"
    #create_base()

if __name__ == '__main__':
    main()

