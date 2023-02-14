from flask import Flask,render_template,request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

df=pd.read_csv('location.csv')
feature_loc=pd.read_csv('with_feature_location.csv')
pipe1=pickle.load(open('Nofeature.pkl','rb'))
pipe2=pickle.load(open('withfeature.pkl','rb'))

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Get the selected city from the form
        city = request.form['city']
        # Get a list of locations for the selected city
        locations = df[df['City'] == city]['Location'].tolist()
        # Return the locations as a JSON response
        return jsonify(locations)
    else:
        # Get a list of all the cities
        cities = df['City'].unique().tolist()
        locations = []
        return render_template('index.html', cities=cities, locations=locations,pythonList=feature_loc['Location'].tolist())


@app.route('/predict',methods=['POST'])
def predict():
    location=request.form.get('location')
    area=float(request.form.get('Area'))
    Bedrooms=int(request.form.get('Bedrooms'))
    Resale=request.form.get('Re-sale')
    if Resale=='Yes':
        Resale=1
    else:
        Resale=0
    
    if request.form.get('check_Features')=='on':
        if request.form.get('checkbox1')=='on':
            PowerBackup=1
        else:
            PowerBackup=0
        if request.form.get('checkbox2')=='on':
            X7Security=1
        else:
            X7Security=0
        if request.form.get('checkbox3')=='on':
            CarParking=1
        else:
            CarParking=0
        if request.form.get('checkbox4')=='on':
            GasConnection=1
        else:
            GasConnection=0
        if request.form.get('checkbox5')=='on':
            ClubHouse=1
        else:
            ClubHouse=0
        if request.form.get('checkbox6')=='on':
            SwimmingPool=1
        else:
            SwimmingPool=0
        if request.form.get('checkbox7')=='on':
            Gymnasium=1
        else:
            Gymnasium=0
        if request.form.get('checkbox8')=='on':
            RainWaterHarvesting=1
        else:
            RainWaterHarvesting=0
        if request.form.get('checkbox9')=='on':
            SportsFacility=1
        else:
            SportsFacility=0
        input=pd.DataFrame([[area,location,Bedrooms,Resale,Gymnasium,SwimmingPool,RainWaterHarvesting,SportsFacility,ClubHouse,X7Security,PowerBackup,CarParking,GasConnection]],columns=['Area', 'Location', 'No_of_Bedrooms', 'Resale','Gymnasium','SwimmingPool','RainWaterHarvesting','SportsFacility','ClubHouse','24X7Security','PowerBackup','CarParking','Gasconnection'])
        prediction=round(pipe2.predict(input)[0],2)
    else:
        input=pd.DataFrame([[area,location,Bedrooms,Resale]],columns=['Area', 'Location', 'No_of_Bedrooms', 'Resale'])
        prediction=round(pipe1.predict(input)[0],2)
    return str(prediction)

if __name__=="__main__":
    app.run(port=5001)

