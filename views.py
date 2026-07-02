# Import these methods
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.sessions.models import Session
import sklearn
import pyzipper
import pickle
import pandas as pd
import numpy as np
import requests
import random
import string
import os
import math
from datetime import datetime
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import smtplib
import mimetypes
from email.message import EmailMessage
from django.core.mail import send_mail
import base64 
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad

def base(request):
    return render(request, 'base.html', {})


def home(request):
    return render(request, 'home.html', {})

def UserLogin(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['Password']
        
        if User_Details.objects.filter(Username=Username, Password=password).exists():
            user = User_Details.objects.get(Username=Username, Password=password)
            
                
            request.session['User_id'] = str(user.id)
            request.session['type_id'] = 'User'
            request.session['username'] = Username
            request.session['User_email'] = user.Email
            request.session['Full_name'] = user.Full_name
            #request.session['Email_pwd'] = E_pwd


            request.session['login'] = 'Yes'
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/UserLogin/')

    else:
        return render(request, 'UserLogin.html', {})







def UserRegisteration(request):
    if request.method == "POST":
        Full_name = request.POST['name']
        Age = request.POST['age']
        Gender = request.POST['gender']
        Phone = request.POST['number']
        Email = request.POST['email']
        Username = request.POST['username']
        Password = request.POST['password']
      
        register = User_Details(Full_name=Full_name, Age=Age,Gender=Gender ,Phone= Phone,Email= Email,Username= Username,Password=Password)
        register.save()
        messages.info(request,'User Register Successfully')
        return redirect('/UserLogin/')
    else:
        return render(request,'UserRegisteration.html',{})
model = pickle.load(open("model_pkl", "rb"))

#y_pred2 = model.predict([[Age,Annual_Income,Spending_Score,Gender_Female]])




def Prediction(request):
    if request.method == "POST":
        key = 'AAAAAAAAAAAAAAAA'
        iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
        Age = request.POST['Age1']
        Gender_Female = request.POST['gender1']
        Annual_Income = request.POST['Income1']
        Spending_Score = request.POST['Score1']
        enc = base64.b64decode(Age)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        Age = unpad(cipher.decrypt(enc),16)
        Age = Age.decode("utf-8", "ignore")
        print(Age)
        enc = base64.b64decode(Gender_Female)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        Gender_Female = unpad(cipher.decrypt(enc),16)
        Gender_Female = Gender_Female.decode("utf-8", "ignore")
        print(Gender_Female)
        enc = base64.b64decode(Annual_Income)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        Annual_Income = unpad(cipher.decrypt(enc),16)
        Annual_Income = Annual_Income.decode("utf-8", "ignore")
        print(Annual_Income)
        enc = base64.b64decode(Spending_Score)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        Spending_Score = unpad(cipher.decrypt(enc),16)
        Spending_Score = Spending_Score.decode("utf-8", "ignore")
        print(Spending_Score)

        age = float(Age.strip())
        gender_female = float(Gender_Female.strip())
        income = float(Annual_Income.strip())
        score = float(Spending_Score.strip())
        input_data = np.array([[age, gender_female, income, score]])

        y_pred2 = model.predict(input_data)
        print(y_pred2)
        y_pred3=np.rint(y_pred2)
        print(y_pred3)
        y_pred3 = math.trunc(y_pred3[0])
        length = 5
        result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
        print(result_str)
        print("Random string of length", length, "is:", result_str)
        last_record = Prediction_Details.objects.order_by('-id').first()
        next_id = last_record.id + 1 if last_record else 1
        print(next_id)
        userid = request.session['User_id']
        email = request.session['User_email']
        print(email)
        Persona = Prediction_Details(Cluster = y_pred3,Password = result_str,User_ID = userid)
        Persona.save()
        print("before email sent", result_str, y_pred3, next_id)
        url = "https://smail.azurewebsites.net/Email.aspx?Title=Persona&emailid={email}&Sub=TestSubject&Msg=The Cluster Detected {y_pred3}.Prediction Id  is {next_id} .Your password is {result_str}".format(result_str=result_str,email = email,y_pred3 = y_pred3,next_id = next_id)
        res = requests.post(url)
        return redirect('/View_Persona/')
    else:

        email = request.session['User_email']
        print(email)
        return render(request,'Prediction.html',{})

      #persona = Prediction_Details(Cluster=Cluster,Password=Password,User_ID=userid)

    

def View_Persona(request):
    if request.method == "POST":
        userid = request.session['User_id']
        Cluster = request.POST['Cluster']
        Password = request.POST['Password']
        Pred_ID = request.POST['id']
        if Prediction_Details.objects.filter(id = Pred_ID,User_ID=userid,Password=Password).exists():
            user = Prediction_Details.objects.get(id = Pred_ID,User_ID=userid)
            clusters = user.Cluster
            clusters = '3'
            print(clusters)
            if clusters == '0':
                return redirect('/cluster0/')
            if clusters == '1':
                return redirect('/cluster1/')
            if clusters == '2':
                return redirect('/cluster2/')
            if clusters == '3':
                return redirect('/cluster3/')
            return render(request,'Give_Recommendations.html',{})
        else:
            messages.info(request,'Wrong Data Input')

            return redirect('/View_Persona/')
    else:
        return render(request,'View_Persona.html',{})

def Give_Recommendations(request):
    if request.method == "POST":
        cluster = request.POST['Cluster']
        current_user = request.session['User_id']
        current_user_name = request.session['username']
        receiver = request.POST['user']
        files = request.FILES['Upload']
        password = ''.join(random.choice(string.ascii_uppercase ) for i in range(4))
        print(password)
        dataType = request.POST['colorRadio']
        user1 = request.POST['user1']
        user2 = request.POST['user2']
        todayDate = datetime.now()
        print(todayDate)
        dates =str(todayDate).split()
        print(dates)
        current_Date = dates[0]
        print(current_Date)
        current_time = dates[1]
        print(current_time)
        userId = User_Details.objects.filter(Full_name = receiver)
        userId = userId[0].id
        info = DataDetails(Sender_ID=current_user,Sender_name=current_user_name,Receiver_ID=userId,Receiver_name = receiver,files = files,date = current_Date,time = current_time,data_type=dataType,password = password,User1 = user1,User2 = user2,cluster_no = cluster)
        info.save()
        return redirect("/")
    else:
        user_name = request.session['username'] 
        print(user_name)
        receiver = User_Details.objects.all()
        receivers = User_Details.objects.exclude(Username=user_name).order_by().values('Full_name').distinct()
        print(receivers)
        return render(request,'Give_Recommendations.html',{'receivers':receivers})

def View_Data(request):
    user_id = request.session['User_id']
    print(user_id)
    if DataDetails.objects.filter(Receiver_ID=user_id).exists():
        users = DataDetails.objects.filter(Receiver_ID=user_id)
        print(users)
        Full_name = request.session['Full_name'] 
        print(Full_name)
        receiver = User_Details.objects.all()
        receivers = User_Details.objects.exclude(Full_name=Full_name).order_by().values('Full_name').distinct()
        return render(request, 'View_Data.html', {'users':users,'receivers':receivers})
    else:
        return render(request, 'View_Data.html', {})
   

def Logout(request):
    Session.objects.all().delete()
    return redirect('/')

def Share(request,id):
    if DataDetails.objects.filter(id=id).exists():
        print(id)
        myObjects = DataDetails.objects.all().filter(id = id)
        print(myObjects)
        name = myObjects[0].id
        print(name)
        return render(request, 'Share.html', {'myObjects':myObjects})
    else:
        return render(request, 'Share.html', {})


def detect(request):
    if request.method == "POST":
        name = request.POST['firstname']
        print(name)
        email = request.POST['email']
        data = request.POST['file']
        currentuser = request.session['username']
        print(currentuser)
        ##Checking if file exists in database and taking the respective data
        if DataDetails.objects.filter(files=data).exists():
            Dinfo = DataDetails.objects.all().filter(files=data)
            print(Dinfo)
            for info in Dinfo:
                datafiles_n = info.files.name
                print(datafiles_n)
                dataT = info.data_type
                print(dataT)
                Senderid =info.Sender_ID
                print(Senderid)
                Sendername = info.Sender_name
                print(Sendername)
                Receivername = info.Receiver_name
                print(Receivername)
                users1 = info.User1
                print(users1)
                users2 = info.User2
                print(users2)

                usern = User_Details.objects.all().values('Username')
                print(usern) 
                filetype1 = "Yes"
                filetype2= "No"
                if(dataT == filetype1) and (name==Sendername or name==users1 or name==users2 or name in usern):
                    data = request.POST['file']
                    datafile = DataDetails.objects.all().filter(files=data)
                    for i in datafile:
                        data_path = i.files.path
                        data_name = i.files.name
                        data_name = data_name.split("/")
                        data_name =data_name[1]
                        print(data_name)
                        message = EmailMessage()
                        sender = 'mailtestingw@gmail.com'
                        print(sender)
                        recipient = email
                        print(recipient)
                        message['From'] = sender
                        message['To'] = recipient
                        message['Subject'] = "Hello From"+currentuser
                        body =  "This is a confidential Data"
                        message.set_content(body)
                        mime_type, _ = mimetypes.guess_type(data_name)
                        mime_type, mime_subtype = mime_type.split('/')
                        with open(data_path, 'rb') as file:
                            message.add_attachment(file.read(),
                                maintype=mime_type,
                                subtype=mime_subtype,
                                filename=data_name)
                            mail_server = smtplib.SMTP_SSL('smtp.mailjet.com')
                            mail_server.set_debuglevel(1)
                            mail_server.login('c99aeca3c5b0ea572f4aa66fe248afcb','c02c96b55045fed17b569ef0a0b67a9b')
                            mail_server.send_message(message)
                            mail_server.quit()
                            return redirect("/")
                elif(dataT == filetype2) and (name==Sendername or name==users1 or name==users2 or name in usern or name not in usern):
                    #Eid_pwd = request.session['Email_pwd']
                    data = request.POST['file']
                    datafile = DataDetails.objects.all().filter(files=data)
                    for i in datafile:
                        data_path = i.files.path
                        data_name = i.files.name
                        data_name = data_name.split("/")
                        data_name =data_name[1]
                        print(data_name)
                        message = EmailMessage()
                        sender = 'mailtestingw@gmail.com'
                        print(sender)
                        recipient = email
                        print(recipient)
                        message['From'] = sender
                        message['To'] = recipient
                        message['Subject'] = "Hello From"+currentuser
                        body =  "This is a confidential Data"
                        message.set_content(body)
                        mime_type, _ = mimetypes.guess_type(data_name)
                        mime_type, mime_subtype = mime_type.split('/')
                        with open(data_path, 'rb') as file:
                            message.add_attachment(file.read(),
                                maintype=mime_type,
                                subtype=mime_subtype,
                                filename=data_name)
                            mail_server = smtplib.SMTP_SSL('smtp.mailjet.com')
                            mail_server.set_debuglevel(1)
                            mail_server.login('c99aeca3c5b0ea572f4aa66fe248afcb','c02c96b55045fed17b569ef0a0b67a9b')
                            mail_server.send_message(message)
                            mail_server.quit()
                            return redirect("/")
                else:
                    #Eid_pwd = request.session['Email_pwd']
                    usersData = User_Details.objects.all().filter(Username = Sendername)
                    for d in usersData:
                        usersemail='mailtestingw@gmail.com'
                        send_mail("Hello from Admin",
                            "Your Data is being leaked from" " " + Receivername + " " "To" + name,
                            email,
                            [usersemail],
                            fail_silently = False)
                    data = request.POST['file']
                    datafile = DataDetails.objects.all().filter(files=data)
                    for i in datafile:
                        datafiles = i.files.path
                        datafiles_n = i.files.name
                        datafiles_n = datafiles_n.split("/")
                        datafiles_n =datafiles_n[1]
                        print(datafiles_n)
                        password = i.password
                        pre = None
                        output = "C:/workspace/Project/Secure_Persona_Prediction/Files/output.zip"
                        com_lvl = 5
                        pyzipper.compress(datafiles,None,output,password, com_lvl)
                        message = EmailMessage()
                        sender = 'mailtestingw@gmail.com'
                        print(sender)
                        recipient = 'priyanevon21@gmail.com'
                        print(recipient)
                        message['From'] = sender
                        message['To'] = recipient
                        message['Subject'] = "Hello From"+currentuser
                        body =  "This is a confidential Data"
                        message.set_content(body)
                        path = "C:/workspace/Project/Secure_Persona_Prediction/Files/output.zip"
                        head_tail = os.path.split(path)
                        print(head_tail)
                        path_file = head_tail[1]
                        print(path_file) 

                        mime_type, _ = mimetypes.guess_type(path_file)
                        mime_type, mime_subtype = mime_type.split('/')
                        with open(path, 'rb') as file:
                            message.add_attachment(file.read(),
                                maintype=mime_type,
                                subtype=mime_subtype,
                                filename=path_file)
                            mail_server = smtplib.SMTP_SSL('smtp.mailjet.com')
                            mail_server.set_debuglevel(1)
                            mail_server.login('c99aeca3c5b0ea572f4aa66fe248afcb','c02c96b55045fed17b569ef0a0b67a9b')
                            mail_server.send_message(message)
                            mail_server.quit()
                    
                    return redirect("/")

                







        return redirect('/')
    else:
        print('wrong user')
        return render(request,'Share.html',{})

def cluster0(request):
    user_name = request.session['username'] 
    print(user_name)
    receiver = User_Details.objects.all()
    receivers = User_Details.objects.exclude(Username=user_name).order_by().values('Full_name').distinct()
    print(receivers)
    return render(request, 'cluster0.html', {'receivers':receivers})

def cluster1(request):
    user_name = request.session['username'] 
    print(user_name)
    receiver = User_Details.objects.all()
    receivers = User_Details.objects.exclude(Username=user_name).order_by().values('Full_name').distinct()
    print(receivers)
    return render(request, 'cluster1.html', {'receivers':receivers})

def cluster2(request):
    user_name = request.session['username'] 
    print(user_name)
    receiver = User_Details.objects.all()
    receivers = User_Details.objects.exclude(Username=user_name).order_by().values('Full_name').distinct()
    print(receivers)
    return render(request, 'cluster2.html', {'receivers':receivers})

def cluster3(request):
    user_name = request.session['username'] 
    print(user_name)
    receiver = User_Details.objects.all()
    receivers = User_Details.objects.exclude(Username=user_name).order_by().values('Full_name').distinct()
    print(receivers)
    return render(request, 'cluster3.html', {'receivers':receivers})