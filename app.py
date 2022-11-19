from flask import Flask,render_template,request
import pandas as pd
import pickle

app = Flask(__name__)

data=pd.read_csv('G:\MINOR-main\MINOR-main\location.csv')
pipe=pickle.load(open('G:\MINOR-main\MINOR-main\\Nofeature.pkl','rb'))
# global city

@app.route('/')
def index():
    locations=data['Location'].unique()
    # locations=data[data['City']==city]['Location'].unique()
    return render_template('index.html',locations=locations)

@app.route('/predict',methods=['POST'])
def predict():
    location=request.form.get('location')
    area=float(request.form.get('Area'))
    city=request.form.get('City')
    Bedrooms=int(request.form.get('Bedrooms'))
    Resale=request.form.get('Re-sale')
    if Resale=='Yes':
        Resale=1
    else:
        Resale=0
    
    input=pd.DataFrame([[area,location,Bedrooms,Resale]],columns=['Area', 'Location', 'No_of_Bedrooms', 'Resale'])
    prediction=round(pipe.predict(input)[0],2)
    return str(prediction)

if __name__=="__main__":
    app.run(debug=True,port=5001)

