from flask import Flask, render_template,request,session,redirect,url_for,Response
from os import listdir
from pymongo import MongoClient
from recommender import Recommender
import shutil
app = Flask(__name__)
client=MongoClient()
db=client["nyd"]
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

r=Recommender()

for i in listdir('projects'):
    i="projects/"+i
    f=open(i).read()
    shutil.move(i,'warehouse/')
    synopsis=r.refineproject(f)
    i=i[9:len(i)-4]
    p={'title':i,'synop':synopsis}
    db.pro.insert(p)
        

@app.route('/nyd')
def home():
    message=request.args.get('message')
  
    
    return render_template('index.html',message=message)


@app.route('/signup',methods=['POST'])
def signup():
    
    d={}
    if request.method=="POST":
        d['fname']=request.form['fname']
        d['lname']=request.form['lname']
        d['email']=request.form['email']
        d['pass']=request.form['pass']
        d['about']=request.form['about']
        db.user.insert(d)
        session['email']=d['email']
        return redirect('/makeprofile')
    
  
        
        
@app.route('/makeprofile',methods=['GET','POST'])

def makeprofile():
    p={}
    
    if request.method=="GET":
        return render_template('makeprofile.html')
    else:
        p['useremail']=session['email']
        p['q1']=request.form['q1']
        p['q2']=request.form['q2']
        p['q3']=request.form['q3']
        p['q4']=request.form['q4']
        p['q5']=request.form['q5']
        p['q6']=request.form['q6']
        s=p['q1']+","+p['q2']+","+p['q4']+","+p['q6']
        query=r.refineproject(s)
        p['query']=query
        db.profile.insert(p)
        return redirect('/recommendation')


@app.route('/recommendation',)
def recommend():
    if session['email']==None:
        return redirect("/nyd")
    
    q=list(db.profile.find({'useremail':session['email']}))[0]['query']
    cursor=list(db.pro.find())
    l=[]
    for p in cursor:
        l.append((p['title'],p['synop']))
    r.addproject(l)
    top3=r.recommendation(q)
    
    return render_template('recommendation.html',top3=top3)
        
@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method=="POST":

        email=request.form['email']
        p=request.form['pass']
     
        q=list(db.user.find({'email':email}))
        
        if len(q)!=0:
            if p==q[0]['pass']:
                session['email']=email
                return redirect('/welcome')
            else :
                message="Invalid email or password"
                return redirect(url_for('home',message=message))
               
        
        else :
            message="Invalid email or password"
            return redirect(url_for('home',message=message))

@app.route('/welcome',methods=['GET','POST'])
def welcome():
    if request.method=="POST" :
        newq=request.form['newquery']
        newq=r.refineproject(newq)
        oldq=list(db.profile.find({'useremail':session['email']}))[0]['query']
        newq=newq+" "+oldq

        db.profile.update({'useremail':session['email']},{'$set':{'query':newq}})
        

        return redirect('/recommendation')

    else :
        if session['email']==None:
            return redirect("/nyd")
        else:
            return render_template('welcome.html')
    
@app.route('/logout')
def logout():
    session['email']=None
    return redirect('/nyd')
               
@app.route("/<path:path>")
def download(path):
    path=path.replace(' ','%20')
    print "yuyyyyu"
    f=open("warehouse/"+path+".txt")
    return Response(f,mimetype="text",headers={"Content-disposition":"attachment; filename=file.txt"})
    
    
if __name__ == '__main__':
    app.run(debug=True)