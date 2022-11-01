from flask import Flask,render_template,request,session
import ibm_db
import re

app=Flask(__name__)
app.secret_key='a'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kmz12090;PWD=Y3bxFYobLHdUjeXy;")


@app.route("/login",methods=['GET','POST'])
def login():
    global userid
    msg=" "
    
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        sql="SELECT * FROM users WHERE username=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.blind_param(stmt,1,username)
        ibm_db.blind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            userid=account["USERNAME"]
            session['username']=account["USERNAME"]
            msg='Logged in successfully!'
            return render_template("dashboard.html", msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('login.html', msg=msg)
            

@app.route("/register",methods=["GET","POST"])
def register():
    msg=" "
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM users WHERE username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.blind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address"
        elif not re.Match(r'[A-Za-z0-9]+',username):
            msg="name must contain only characters and numbers"
        else:
            insert_sql="INSERT INTO users VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.blind_param(prep_stmt,1,username)
            ibm_db.blind_param(prep_stmt,2,email)
            ibm_db.blind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg='you have successfully Logged in!'
            
    elif request.method=='POST':
        msg='please fill out of the form'
        return render_template('register.html', msg=msg)


if __name__=='__main':
 app.run(host='0.0.0.0')
        