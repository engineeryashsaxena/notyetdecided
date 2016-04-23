from flask import Flask, render_template,request,session,redirect
from os import listdir
from pymongo import MongoClient
from recommender import Recommender
import shutil
r=Recommender()
client=MongoClient()
db=client["nyd"]
for i in listdir('projects'):
    i="projects/"+i
    f=open(i).read()
    shutil.move(i,'warehouse/')
    synopsis=r.refineproject(f)
    i=i[9:len(i)-4]
    p={'title':i,'synop':synopsis}
    db.pro.insert(p)
    
    