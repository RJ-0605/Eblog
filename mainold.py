


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
    post_exists=False
    adminstat=False
    logstatus=False
    username=False
    cur = mysql.connection.cursor()

    try:
        
        cur.execute( 'SELECT * FROM  UserPost ')
        post=cur.fetchall()
        if post_exists :
            for row in post_exists:            
                session['post_title']=row.get('post_title')
              # session['post_title']=post('postitle')
                post_title=session['post_title']

      # sideright=''
        if 'loggedin' in session :
            logstatus=True
            username=session['username']
            adminstat=session['status']
               

    except mysql.connection.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        cur.close()
    return render_template("indexflask.html", logstatus=logstatus, adminpriv=adminstat,username=username,post=post_exists)





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
    adminstat=False
    logstatus=False
    username=False
    if 'loggedin' in session :
        logstatus=True
        username=session['username']
        if session['status']=='admin':
            adminstat=session['status']     
    
    return render_template("about.html", logstatus=logstatus, adminpriv=adminstat, username=username)


@app.route('/aboutus' )
def aboutus():
    adminstat=False
    logstatus=False
    username=False
    if 'loggedin' in session :
        logstatus=True
        username=session['username']
        if session['status']=='admin':
          adminstat=session['status']

      
    return render_template("about.html", logstatus=logstatus, adminpriv=adminstat, username=username)
    
  
# serves as some kinda of admin for the owners of the blog
@app.route('/manageblog' )
def manageblog():
    homepage=''
    post=""
    adminstat=False
    logstatus=False
    username=False
   # sideright=''
    if 'loggedin' in session :
        logstatus=True
        username= session['username']
        adminstat=session['status']
        cur= mysql.connection.cursor()
        if session['status']=='admin':
            try:
                
                post=cur.fetchone()
                if post :
                    for row in post:
                  
                        session['post_title']=row.get('post_title')  
                        post_title=session['post_title']            
          

              # session['post_title']=post('postitle')
                 
          
          
        
            except mysql.connection.Error as e:
                print("Error reading data from MySQL table", e)
            finally:
                cur.close() 

    
        return render_template("blogpostedit.html", username=username, logstatus=logstatus, adminpriv=adminstat ,post=post )

    return render_template("indexlayout.html", username=username, logstatus=logstatus, adminpriv=adminstat ,post=post )    






@app.route('/useradmin', methods=['POST','GET'])
def useradmin():
  

      if session['status']=='admin':
        
            msg=''

            if request.method == 'POST':        
              
                  image=request.files['bpicture']
                  title=request.form.get('post_title')
                  pgraph1=request.form.get('pgraph1')
                  pgraph2=request.form.get('pgraph2')
                  pgraph3=request.form.get('pgraph3')
                  qoute=request.form.get('qoute')
                  qoute_ref=request.form.get('qoute_ref')
                  pgraph6=request.form.get('pgraph6')
                  pgraph7=request.form.get('pgraph7')

                  dateuser='January 1,2017'
                  timeuser= '12:00 PM'

                  # blogcomments=request.form.get('blogcomments')
                  # get username from session base at the top and add 
                  useremail= session['email']
                  username= session['username']
                  filename=image.filename
                  image.save('./static/images/uploads/'+filename)
                  imagesavdsucesful= True

                  cur = mysql.connection.cursor()

                  if imagesavdsucesful :

                      try:

                        post_title=session['post_title']
                        
                        cur.execute( 'SELECT * FROM  UserPost WHERE post_title=%s ', ( post_title , ))
                        post_exist=cur.fetchone()

                        if post_exist:
                          # if the title exists then update info
                            cur.execute("UPDATE albums SET username=%s, useremail=%s, post_title=%s, post_image=%s, par1=%s , par2=%s , par3%s , qoute=%s , qoute_reference=%s , par6=%s ,par7=%s, timeuser=%s ,post_title=%s WHERE post_title=%s", ( username , useremail, title, image , post_title, pgraph1, pgraph2, pgraph3, qoute, qoute_ref , pgraph6 , pgraph7 ,post_title  ) )

                            mysql.connection.commit()
                        
                            print(cur.rowcount, "Record updated.")

                        else:
                            sql = "INSERT INTO UserPost (username , useremail, post_title, post_image , par1 ,par2 , par3 , qoute , qoute_reference ,par6 , par7 , dateuser , timeuser )VALUES (%s, %s , %s , %s , %s, %s , %s , %s, %s, %s , %s , %s , %s )"
                            val=(username , useremail, title, image, pgraph1, pgraph2, pgraph3, qoute, qoute_ref , pgraph6 , pgraph7,dateuser,timeuser )

                            cur.execute(sql, val)

                            done=mysql.connection.commit()
                            if done:
                                print(cur.rowcount, "Record inserted.")

                            else:
                                msg='Image not saved successful,Record not updated'
                                print("Record not updated.")

                          # manage blog will be here to load data 
                        return redirect(url_for('manageblog'))


                      except mysql.connection.Error as e:
                          print("Error reading data from MySQL table")
                          msg='Image not saved successful,Record not updated'
                          print("Record not updated.")
                        
                      finally:  
                          cur.close()
              

            else:
              # POST not successfull
                msg='Image not saved successful'
                print("Image not saved successful, to advanced to stage of saving records")
                return redirect(url_for('manageblog'))

        
      return redirect(url_for('home'))



# @app.route('/adminfunc', methods=['POST','GET'])
# def adminfunc():

#   msg=''

#   if request.method == 'POST':
#     image=request.files['bpicture']
#     title=request.form.get('blogtitle')
#     blogcomments=request.form.get('blogcomments')

#     username='kobby'
#     filename=image.filename
#     image.save('./static/imgs/uploads/'+filename)
#     imagesavdsucesful= True

#     if imagesavdsucesful :

#       cur = mysql.connection.cursor()

#       sql = "INSERT INTO Blogtable (title,blogcomments,username,image)VALUES (%s, %s , %s,%s)"
#       val=(title,blogcomments,username,filename)

#       cur.execute(sql, val)

#       mysql.connection.commit()

#       print(cur.rowcount, "Record inserted.")

#     else:
#       msg='Image not saved successful'
#       print("Record not inserted.")

# #these are outside they post so they work with the automatic get request
#   # cur = mysql.connection.cursor()
#   # cur.execute( 'SELECT * FROM  Blogtable')
#   # blogdetails=cur.fetchall()

#   return render_template('admin.html')


# @app.route('/signupblog' )
# def signupblog():

#    # sideright=''
#   return render_template("signupblog.html")

# @app.route('/loginblog' )
# def loginblog():

#    # sideright=''
#   return render_template("loginblog.html")







# @app.route('/contactblog' )
# def contactblog():
#   contactpage=''
#   if 'loggedin' in session :
#     displaynoemail=True
#     return render_template("contactblog.html",contactpage=contactpage,display='displaynoemail')
#    # sideright=''
#   return render_template("contactblog.html", contactpage=contactpage)


# @app.route('/userfunc',methods = ['POST', 'GET'])
# def userfunc():

#   if 'email' in session :

#     emailmsg=session['email']
#     # return render_template("contactblog.html",display='displaynoemail')
 

#   if request.method == 'POST':
    
#     message=request.form.get('msg')
#     usertype='Normal'
    
#     if 'email' in session :
#       usertype='Priority'
#     else  :
#       emailmsg=request.form.get('email')


      
    
#     if emailmsg :
#       cur = mysql.connection.cursor()
#       sql = "INSERT INTO UserMessages (UserType,UserEmail,Message)VALUES (%s,%s,%s)"
#       val=(usertype,emailmsg,message)

#       cur.execute(sql, val)

#       mysql.connection.commit()

#       print(cur.rowcount, "record inserted.")
#       # any sending of mail to me  will be done here 
#       loginmail='rodneytetteh@gmail.com'
#       user = 'rodneytetteh@gmail.com'

#       # insert app_password here in the future instead of describing it at the beginning

#       host = 'smtp.gmail.com'
#       port = 465
#       to = 'jedikwao@gmail.com'

#       # subject = 'Moro Blog Comments  Sent from   '+ emailmsg
#       subject = 'Moro Blog Comments '
#       # message main content 
#       content = message +'\n'+'Sent by\n ' + emailmsg
      

#       ### Define email ###
#       message = MIMEMultipart()
#       # add From 
#       message['From'] = Header(user)
#       # add To
#       message['To'] = Header(to)     
#       # add Subject
#       message['Subject'] = Header(subject)
#       # add content text
#       message.attach(MIMEText(content, 'plain', 'utf-8'))
          
#       ### Send email ###
#       server = smtplib.SMTP_SSL(host, port) 
#       server.login(loginmail, app_password)
#       server.sendmail(user, to, message.as_string()) 
#       server.quit() 
#       print('Sent email successfully')
            



#   return redirect(url_for('contactblog'))



# @app.route('/aboutinsert')
# def aboutinsert():
#    sideright=''
#    aboutpage=''
#    return render_template("aboutinsert.html",aboutpage=aboutpage)


@app.route('/regfunc',methods = ['POST', 'GET'])
def regload():

    # mysql too many connections solution in on the next line 
   mysql.connection.cursor().close()

   registerpage=''
   loginpage=''
   # redirect from the register function i set a variable here 
    # and catch it if it exists that is if 

   msg=''
   if request.method == 'POST':
      firstname = request.form.get('fname')
      lastname = request.form.get('lname')
      username = str(request.form.get('username'))
#       date_ofbirth=str(request.form.get('birthday'))
#       # date_ofbirth='bread'

      email = str(request.form.get('email')).lower()
      passwd = request.form.get('password')
      confirm_passwd = request.form.get('confirm_password')
      temporal_image="yourprofilepic.jpg"

      # i will go and do the stats changes myself for normal user
       # and admin users
      # status="admin"
      
      status="normal"
#       # we create a temporal  instance that can store the results from the validorex script  
      validated=Register_validator(firstname,lastname,username,email,passwd,confirm_passwd)
      
#      # now we can access the function since the instance has been set 
      if validated.validator():

#          # now about to crosscheck if username and email , data does not already exist in database before proceeding 
         cur = mysql.connection.cursor()

         # cur.execute('USE sql7364406')

         # cur.execute( 'SELECT * FROM  RegisterAccount WHERE username=%s  AND email=%s' , ( username , email,))
         # account=cur.fetchone()

         cur.execute( 'SELECT * FROM  RegisterAccount WHERE username=%s ', ( username , ))
         uaccount=cur.fetchone()

         cur.execute( 'SELECT * FROM  RegisterAccount WHERE  email=%s' , (  email,))
         eaccount=cur.fetchone()

         # if account or uaccount or eaccount :
         if uaccount or eaccount :



            msg=f"An account with this username  {username} or email {email} already exists"
         
            # return redirect(url_for('register', reg_username=msg))

            return render_template('register.html',reg_msg=msg)

#             # else if there was no successful retrieval that means that information does not exist so we can add new input to the RegisterAccount
         else:

            sql = "INSERT INTO RegisterAccount (firstname,lastname,username,status,profile_image,email,password)VALUES (%s, %s , %s,%s,%s,%s,%s)"

            val=(firstname,lastname,username, status,temporal_image,email,passwd,)

            cur.execute(sql, val)

            mysql.connection.commit()

            print(cur.rowcount, "record inserted.")

            # close the mysql connection and the cursor
            cur.close()
            mysql.connection.close()
            print("MySQL connection is closed")

            loginmail='rodneytetteh@gmail.com'
            user = 'rodneytetteh@gmail.com'

      # insert app_password here in the future instead of describing it at the beginning

            # host = 'smtp.gmail.com'
            # port = 465
            # to = email

            # subject = 'Moro Corp'
            # # message main content 
            # content = 'You have been registered successfully a number will be sent to you '
            

            # ### Define email ###
            # message = MIMEMultipart()
            # # add From 
            # message['From'] = Header(user)
            # # add To
            # message['To'] = Header(to)     
            # # add Subject
            # message['Subject'] = Header(subject)
            # # add content text
            # message.attach(MIMEText(content, 'plain', 'utf-8'))
                
            # ### Send email ###
            # server = smtplib.SMTP_SSL(host, port) 
            # server.login(loginmail, app_password)
            # server.sendmail(user, to, message.as_string()) 
            # server.quit() 
            # print('Sent email successfully')
            
            
            
            
#             # redirect from the register function  to the login function 
#             # i set a variable here 
#              # and catch it if it exists that is if 
            msg=f"Account {username} created successfully "
            
            return redirect(url_for('login'))

         

      else:
         # 
         msg = "Please fill out form "
         # return redirect(url_for('register', reg_username=msg))
         # return render_template('register.html',registerpage=registerpage, reg_username=msg)
         
         
   return render_template('register.html',registerpage=registerpage, reg_msg=msg)






@app.route('/loginfunc',methods = ['POST'])
def loginload():
    # use the mysql connection code below to after running another mysql client 
    # code such as pymysql or mysql.connector to make 
    # the reset number of times conneciton has been made 
   # mysql.connection.cursor().close()

   msg=""

   loginpage=''

   if request.method == 'POST':

      usernamemail = str(request.form.get('usernam_email')).lower()
      
      passwd = request.form.get('password')

      print("WORKS",usernamemail, passwd)

#       # we create a temporal  instance that can store the results from the validorex script  
      validateduseremail = Login_validator(usernamemail,passwd) 

      
      
#      # now we can access the function since the instance has been set 
      if validateduseremail.validator():
         cur = mysql.connection.cursor()

#          # cur.execute('USE myfirstdatabase')

#          # try fetching  from either username also try fetching from email , usernamemail in general refers to input that can hold both email    
#     # and    username 
#     # per what is given as an input 

         cur.execute( 'SELECT * FROM  RegisterAccount WHERE username=%s OR email=%s' , ( usernamemail , usernamemail, )  )
         ueaccount=cur.fetchone() 

         

         cur.execute( 'SELECT * FROM  RegisterAccount WHERE  password=%s' , (  passwd,))
         paccount=cur.fetchone()

            
         if  ueaccount and  paccount:
            cur.execute( 'SELECT username FROM  RegisterAccount WHERE username=%s OR email=%s' , ( usernamemail , usernamemail, )  )
            usnmaccount=cur.fetchone()
            
#             # the username a key to generate the information 
#             # there because i used Dictcursor property
            usname=usnmaccount['username']

            # close mysql connection after everything both cursor and database connection
            # but in this case we jsut going to disconnect the cursor 
            # and close the database at logout
            cur.close()
            mysql.connection.close()
            print("MySQL connection is closed")
            
#             #  session begins here we can use the id of the the row that the ueaccount 
#             # gave to us or the id that the password paccount gave to us 
#             # since SELECT * picks the entire row where a particular column with a value is used to inspect.
            
            session['loggedin']=True
#             session['id']= ueaccount['id']
            session['username']=ueaccount['username']
            session['email']=ueaccount['email']
             # that entire row has been selected so i can select what i want from it 
            session['status']=ueaccount['status']

            if session['status']=='admin':
              session['adminpriv']=True



              # return render_template("indexflask.html", login_username=usname)
              return redirect(url_for('home'))

         else:
            msg= "invalid login details "



      else:

         # this is thrown because of the LoginVlidator in validatorex
         msg= "invalid login syntax or login field is empty"





      return  render_template('signin.html',loginpage=loginpage,login_msg=msg)






@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)

   session.pop('adminpriv', None)

   session.pop('email', None)
   session.pop('status',None)
   # Redirect to login page
   return redirect(url_for('home'))



















@app.route('/about')
def about():

#  return ("<h1>Hello World</h1>
   return render_template("about.html",title=about)

# this shows the main route url name i choose is independent of the function 
# just thst it helps in the future to make your work less complicated and helps you understand the linkage
#   url_for function helps you generate  the right url for the function logincheck 
# irrespective of the name change i made to 
#         make it logincheck

@app.route('/regcheckZ/<alertdiv>')
def regcheck(alertdiv):
   if alertdiv :
      
      return render_template("register.html",alertmssgs=alertdiv)

   else:
      return render_template("register.html")



# @app.route('/register')
# def register():

#    return render_template("register.html")

# @app.route('/login')
# def login():

#    return render_template("login.html")



@app.route('/success/<name>')
def success(name):
    
    return render_template("index.html")


# this will load future validator functions when the validator class 
# on seperate python script has been imported here
   



@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500



     

# if __name__ == '__main__':
   # app.run(debug = True)




if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
# [END gae_flex_quickstart]
