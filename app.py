from flask import Flask, jsonify, render_template, request
import json
import pickle
import pandas as pd
import numpy as np

import csv

import smtplib 

from email.message import EmailMessage

from string import Template

from pathlib import Path


filename= 'Final_Project.sav'
model= pickle.load(open(filename, 'rb'))

# MY_ADDRESS,PASSWORD='hello.hell3096@gmail.com','Hello.hell#3096'

MY_ADDRESS,PASSWORD='no.reply.healthpredictor@gmail.com','Health@Predictor18'




app = Flask(__name__)

@app.route('/', methods= ['POST','GET'])
def home() :
   return render_template('index.html')

@app.route('/profile', methods= ['POST','GET'])
def profile() :
   return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
  
    if request.method=="POST" or request.method=="GET":
        try:
            data=request.form.to_dict()
            # print(data)
            send_mail_user(data)
           
            
            
            return render_template('/thankyou.html',name=data['username'])
        except Exception as e:
            # print(e)
            return f"did not save to database {e}"
    else:
        return "something went wrong" 



def write_to_file(data):
    with open(r'mental_health.txt',mode='a') as db:
        email=data['email']
        name=data['username']
        gender = data["Gender"]
        treatment= data["Treatment"]
        tret_prob = data["Treatment Probability"]


        file=db.write(f'\n {name} ,{email},{gender},{treatment},{tret_prob}')

def write_to_csv(data):
 
    with open(r'mental_health.csv',mode='a',newline='') as db2:
        email=data['email']
        name=data['username']
        gender = data["Gender"]
        treatment= data["Treatment"]
        tret_prob = data["Treatment Probability"]
        
        csv_writer = csv.writer(db2,delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,gender,treatment,tret_prob])
        print(csv_writer)



def send_mail(data):
   
    email=EmailMessage()
     
    email['from'] = 'Mental Health  Predictor '
    email['to'] = data["email"]

    email['subject'] = f'Hey {data["username"]} Your Prediction Results Are'
    data["message"] = f' You Should {data["Treatment"]}  Probability is   {data["Treatment Probability"]} \n Please Visit our website for More Details'
    msg=f" \t Mental_Health_ Predictor \n Name:{data['username']} \n EMAIL : {data['email']} \n SUBJECT :   Prediction Details \n MESSAGE : {data['message']}"


    email.set_content(msg)


    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MY_ADDRESS,PASSWORD)
        smtp.send_message(email)
        print('all good AK ')


def send_mail_user(data):
   
    email=EmailMessage()
     
    email['from'] = 'Mental_Health_Predictor WebApp'
    email['to'] = "rajamonianil0909@gmail.com"
    email['subject'] = " Hey ! AK You Have New Response From Heart Predictor Web App "
    msg=f" \t From Heat Predictor WebApp \n Name:{data['username']} \n EMAIL : {data['email']} \n SUBJECT : {data['subject']} \n MESSAGE : {data['message']}"


    email.set_content(msg)


    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MY_ADDRESS,PASSWORD)
        smtp.send_message(email)
        print('all good AK')

@app.route('/result', methods= ['POST','GET'])
def result():
    if request.method == 'POST':
        input= request.form

        mh_predict = pd.DataFrame({
            'Gender': [input['Gender']],
            'Self_Employed': [input['Self_Employed']],
            'Family_History': [input['Family_History']],
            'Work_Interfere': [input['Work_Interfere']],
            'Employee_Numbers': [input['Employee_Numbers']],
            'Tech_Company': [input['Tech_Company']],
            'Benefits': [input['Benefits']],
            'Care_Options': [input['Care_Options']],
            'Seek_Help': [input['Seek_Help']],
            'Anonymity': [input['Anonymity']],
            'Medical_Leave': [input['Medical_Leave']],
            'Mental_Health_Consequence': [input['Mental_Health_Consequence']],
            'Coworkers': [input['Coworkers']],
            'Supervisor': [input['Supervisor']],
            'Mental_Health_Interview': [input['Mental_Health_Interview']],
            'Physical_Health_Interview': [input['Physical_Health_Interview']],
            'Mental_VS_Physical': [input['Mental_VS_Physical']],
            'Observed_Consequence': [input['Observed_Consequence'],]
        })

        prediksi= model.predict_proba(mh_predict)[0][1]
        print("prediction",model.predict(mh_predict))

        if prediksi>0.75:
            pred= 'Get Treatment'
        else:
            pred= 'Get No Treatment'

        data = {"username":input["username"],
                "Age":input["Age"],
                "email":input["email"],
                "Gender":input["Gender"],
                "Treatment":pred,
                "Treatment Probability":prediksi}

        write_to_csv(data)
        send_mail(data)
        write_to_file(data)
        print(data)
        return render_template('result.html', data= input, pred= pred, prob= round(prediksi, 2))

if __name__ == '__main__':
    
    app.run()
