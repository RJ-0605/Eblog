
class Register_validator:

#  In the near future will be receiving the date of registration and time as an input from the main.py


    def __init__(self,firstname,lastname,username,email,passwd,confirm_passwd):
        self.email = email
        self.passwd = passwd
        self.confirm_passwd = confirm_passwd
        self.firstname = firstname
        self.lastname = lastname
        self.username=username



    def validator(self):
        if self.firstname and self.lastname and self.username and  self.passwd and self.confirm_passwd and self.email != "" and self.passwd == self.confirm_passwd and len(str(self.passwd)) >= 6 :
            print('Meets all requirements')
            return True
        else:
            return False



class Login_validator:



    def __init__(self,usernmemail,passwd):
        
        self.usernmemail=usernmemail
        self.passwd = passwd  
        
# in the near future i would pass the regex checks here or in the main.py 
# since i have taken that funcitonatlity away by distorting the input type in the html 

    def validator(self):
        if  self.usernmemail and self.passwd != "":
            print('Meets all requirements')
            return True
        else:
            return False

