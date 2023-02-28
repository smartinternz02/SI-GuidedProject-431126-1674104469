from flask import Flask, render_template,redirect
import random
import numpy as np
import pickle
import pandas as pd
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "BNG96LQnfYy9aApmogueagE8YISwzHDy-ZSJLIy49ioB"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route("/")
def home():
    return render_template('base.html')


@app.route('/m_predict',methods=['POST'])
def mpred():
    return render_template('Manual_predict.html')
@app.route('/s_predict',methods=['POST'])
def spred():
    return render_template('Sensor_predict.html')

#Manual

@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test=([[int(x) for x in request.form.values()]])
    print(x_test)
    a=model.predict(x_test)
    pred=a[0]
    if(pred == 0):
        pred="No failure expected with in 30 days"
    else:
         pred="Maintenance Required!! Expected a failure with in 30 days"
    return render_template('Manual_predict.html',prediction_text=pred)
       

#Sensor

@app.route('/sy_predict',methods=['POST'])
def sy_predict():
    inp1=[]
    inp1.append(random.randint(0,100)) #id 
    inp1.append(random.randint(0,365)) #cycle
    for i in range(0,25):
        inp1.append(random.uniform(0,1))
        #inp1.append(random.randint(0,365)) #ttf
    pred=model.predict([inp1])
    if (pred == 0):
            pred = "No failure expected within 30 days."
    else:
           pred = "Maintenance Required!! Expected a failure within 30 days." 
    
    payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/21e73c06-1ab4-4156-8fd3-a960713f5f37/predictions?version=2023-02-10', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    
    return render_template('Sensor_predict.html', prediction_text=pred, data=inp1)

    
if __name__ == '__main__':
    app.run(debug=False)    
  