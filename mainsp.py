



from flask import Flask, redirect, url_for, request, render_template,session
from validatorex import Register_validator , Login_validator

from flask_mysqldb import MySQL

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import os


app = Flask(__name__)

# must later genrate a sepearate function or import for generating 
# seperate key for session .

app.secret_key = '67fe0e4d2a60c56aac5b2362b1ded716'

# code for starting xampp  sudo /opt/lampp/lampp start
# 
# Database of MySQl with flask


#    these configurations helped with connecting xampp mysql server
#     with flask-mysqldb 

#  app.config['MYSQL_UNIX_SOCKET']='/opt/lampp/var/mysql/mysql.sock'    
#  app.config['MYSQL_PORT']=3306


#     Now all the SUPER USERS can be used interchangeably 

#     both this 

#     app.config['MYSQL_USER']='root'
#            and 
#     app.config['MYSQL_USER']='jedidiah'

#  as they are all using the xampp database
#  because of the socket provided


# the unixsocket is necessary for mysql ,due to xampp ,to work
app.config['MYSQL_UNIX_SOCKET']='/opt/lampp/var/mysql/mysql.sock'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='FirstBlog'

# the configs below are for remote copy of database with mirror structure of firstdatabase

# app.config['MYSQL_HOST']='sql7.freemysqlhosting.net'
# app.config['MYSQL_PORT']=3306
# app.config['MYSQL_USER']='sql7364406'
# app.config['MYSQL_PASSWORD']='fQtnb5UWCq'
# app.config['MYSQL_DB']='sql7364406'

app.config['MYSQL_CURSORCLASS']='DictCursor'

app.config['upload_image']='./static/images/uploads'

mysql=MySQL(app)



app_password = 'kbdrukfcjqghmrum'




msg=""

@app.route('/')
@app.route('/home')
def home():
  homepage=''
  no_images=True  
  
  post=False
  adminstat=False

  try:
    cur = mysql.connection.cursor()     
    cur = cur.DictCursor

    cur.execute( 'SELECT * FROM  UserPost ')
    post=cur.fetchone()
    if post :
      for row in post:
        
        session['post_title']=row.get('post_title')
      # session['post_title']=post('postitle')
        post_title=session['post_title']

    # sideright=''
    if 'loggedin' in session :
      if session['status']=='admin':  
        adminstat=session['status']
             
      return render_template("indexflask.html", logstatus=True, adminpriv=adminstat,username=session['username'],post=post)
  # else:
  # loggedout=False
  #    return redirect(url_for('login'))

  except mysql.connection.Error as e:
    print("Error reading data from MySQL table", e)
  finally:
    cur.close()
  return render_template("indexflask.html", logstatus=False)





@app.route('/register' )
def register():
  homepage=''
   # sideright=''
  return render_template("register.html")

@app.route('/login' )
def login():
  homepage=''
   # sideright=''
  return render_template("signin.html")

@app.route('/limitedit' )
def limitedit():
  homepage=''
   # sideright=''
  return render_template("blog2edit.html")

@app.route('/contactus' )
def contactus():
  homepage=''
  adminstat=False
  if 'loggedin' in session :

      if session['status']=='admin':  
        adminstat=session['status']      
  return render_template("contact.html", logstatus=True, adminpriv=adminstat, username=session['username'])
  return render_template("contact.html", logstatus=False)


@app.route('/aboutus' )
def aboutus():
    adminstat=False
    if 'loggedin' in session :
        if session['status']=='admin':
          adminstat=session['status']
      
        return render_template("about.html", logstatus=True, adminpriv=adminstat, username=session['username'])
    return render_template("about.html", logstatus=False)

  