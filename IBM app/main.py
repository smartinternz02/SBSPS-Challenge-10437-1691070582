from flask import Flask,render_template,request
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import joblib
import requests

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def hello_world():
    pred_val=[]
    res = []
    x = ''
    ans = []
    if request.method=="POST":
        age = request.form["Age"]
        pred_val.append(age)
        gender = request.form["Gender"]
        pred_val.append(gender)
        stream = request.form["Stream"]
        pred_val.append(stream)
        intern = request.form["Internship"]
        pred_val.append(intern)
        cgpa = request.form["CGPA"]
        pred_val.append(cgpa)
        hostel = request.form["Hostel"]
        pred_val.append(hostel)
        bl = request.form["Backlogs"]
        pred_val.append(bl)
        res = [float(x) for x in pred_val]
        # res = np.array([float(x) for x in pred_val])
        # x = joblib.load("model/model.pkl")
        # ans = (x.predict_proba(res))[0][1]
        

        API_KEY = "fUJdexgpeYNTshYDkfDV4NaCE51g0arg8TkG6P_X9-uM"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
        API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": [
                                        "f0",
                                        "f1",
                                        "f2",
                                        "f3",
                                        "f4",
                                        "f5",
                                        "f6"
                                ], "values": [res] }]}

        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/dc5392e2-be74-4e5f-9c44-3f0477d2d768/predictions?version=2021-05-01', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
    return render_template("index.html", out="Probabilty of you getting placed: "+str(res)+"%")



if __name__=="__main__":
    app.run(debug=True)