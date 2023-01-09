from flask import Flask,render_template,request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

df=pd.read_csv('location.csv')
pipe=pickle.load(open('Nofeature.pkl','rb'))

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
        return render_template('index.html', cities=cities, locations=locations)


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
    
    input=pd.DataFrame([[area,location,Bedrooms,Resale]],columns=['Area', 'Location', 'No_of_Bedrooms', 'Resale'])
    prediction=round(pipe.predict(input)[0],2)
    return str(prediction)

if __name__=="__main__":
    app.run(debug=True,port=5001)

