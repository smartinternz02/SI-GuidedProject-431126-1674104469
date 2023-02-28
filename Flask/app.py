from flask import Flask, render_template, request,redirect
import random
import numpy as np
import pickle
import pandas as pd

model = pickle.loads(open("engine_model.pkl",'rb').read())
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
    return render_template('Sensor_predict.html', prediction_text=pred, data=inp1)

    
    
    
if __name__ == '__main__':
    app.run(debug=False)    
  
