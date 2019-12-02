import flask
from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import pandas as pd
import urllib
import simplejson

app = Flask(__name__)

#Establishing connection
client = MongoClient("mongodb://localhost:27017/")
db=client.mydb

#sotring collection varaibles

col=db.inventory
col1=db.checkout

col1.aggregate([{
                            "$match" : { "fiction": 1 }
                              },
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":-1}},{"$limit":10},{ "$out" : "fiction" }],allowDiskUse=True)


col1.aggregate([{
                            "$match" : { "mystery": 1 }
                              },
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":-1}},{"$limit":10},{ "$out" : "mystery" }],allowDiskUse=True)

col1.aggregate([{
                            "$match" : { "drama": 1 }
                              },
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":-1}},{"$limit":10},{ "$out" : "drama" }],allowDiskUse=True)

col1.aggregate([{
                            "$match" : { "literature": 1 }
                              },
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":-1}},{"$limit":10},{ "$out" : "literature" }],allowDiskUse=True)





def statistics(year,genre):

    col1.aggregate([{
                            "$match" :{ "Year":year,genre: 1 }
                              },
                    
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":-1}},{"$limit":1},{ "$out" : "fav" }],allowDiskUse=True)
    
    print("\nThe most checked out book was: \n")
    pprint(list(db.fav.find()))
    
    col1.aggregate([{
                            "$match" :{ "Year":year,genre: 1 }
                              },
                    
                            {"$group":{"_id":{"BibNumber":"$BibNumber","Title":"$Title","Author":"$Author"},"count":{"$sum":1}}},
                            {"$sort":{"count":1}},{"$limit":1},{ "$out" : "low" }],allowDiskUse=True)
    print("\nThe least checked out book was: \n")
    pprint(list(db.low.find()))


#Function to find books based on author
def find(author):
    results=col.find({"Author":{"$regex":author}},{"Author","Title","Publisher"})
#     pprint(list(results))
    for result in list(results):
            print('\n{0},\n{1},\n{2}\n'.format(result['Author'],result['Title'],result['Publisher']))
    if not list(results):
        print('No such Author')
    
        
    

def suggest(genre):
    

    if genre=='fiction':
        pprint(list(db.fiction.find()))
        
    elif genre=='mystery':
        pprint(list(db.mystery.find()))
        
    elif genre=='drama':
        pprint(list(db.drama.find()))
        
    elif genre=='literature':
        pprint(list(db.literature.find()))
    
    else:
        print('Genre does not exist')
    
        
        

def insert(b,t,a,p,s,i):
    col.insert_one({"BibNum":int(b),"Title":t,"Author":a,"Publisher":p,"Subject":s,"ItemType":i})


def check(o):
    if(o not in range(1,6)):
        print("Wrong option selected")

def update(o):
    
    if o==1:
        col.update_one({"BibNum":int(b)},{"$set": { "Title": x}})

    elif o==2:
        col.update_one({"BibNum":int(b)},{"$set": { "Author": x}})

    elif o==3:
        col.update_one({"BibNum":int(b)},{"$set": { "Publisher":x}})

    elif o==4:
        col.update_one({"BibNum":int(b)},{"$set": { "Subject": x}})

    elif o==5:
        col.update_one({"BibNum":int(b)},{"$set": { "ItemType": x}})
    else:
        print("Wrong BibNumber inserted")
    

                                                                                        