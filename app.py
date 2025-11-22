import os
import pickle
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '123456789'

# Example user database (replace with actual DB)
users = {
    "user@example.com": generate_password_hash("password123")
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_password_hash = users.get(email)
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['user'] = email
            return redirect(url_for('home'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Load Models
base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, "saved_models")

diabetes_model = pickle.load(open(os.path.join(model_dir, "diabetes_model.sav"), "rb"))
heart_disease_model = pickle.load(open(os.path.join(model_dir, "heart_model.sav"), "rb"))
parkinsons_model = pickle.load(open(os.path.join(model_dir, "parkinsons_model.sav"), "rb"))

# --- Routes ---

@app.route('/')
@login_required
def home():
    return render_template('home.html')

# 1. Diabetes Prediction
@app.route('/diabetes', methods=['GET', 'POST'])
@login_required
def diabetes():
    prediction_text = ""
    if request.method == 'POST':
        try:
            # Get data from form
            features = [
                float(request.form['pregnancies']),
                float(request.form['glucose']),
                float(request.form['bloodpressure']),
                float(request.form['skinthickness']),
                float(request.form['insulin']),
                float(request.form['bmi']),
                float(request.form['dpf']),
                float(request.form['age'])
            ]
            
            # Predict
            prediction = diabetes_model.predict([features])
            
            if prediction[0] == 1:
                prediction_text = "Result: The person is diabetic."
            else:
                prediction_text = "Result: The person is NOT diabetic."
                
        except Exception as e:
            prediction_text = f"Error: {str(e)}. Please check inputs."

    return render_template('diabetes.html', result=prediction_text)

# 2. Heart Disease Prediction
@app.route('/heart', methods=['GET', 'POST'])
@login_required
def heart():
    prediction_text = ""
    if request.method == 'POST':
        try:
            features = [
                float(request.form['age']),
                float(request.form['sex']),
                float(request.form['cp']),
                float(request.form['trestbps']),
                float(request.form['chol']),
                float(request.form['fbs']),
                float(request.form['restecg']),
                float(request.form['thalach']),
                float(request.form['exang']),
                float(request.form['oldpeak']),
                float(request.form['slope']),
                float(request.form['ca']),
                float(request.form['thal'])
            ]

            prediction = heart_disease_model.predict([features])

            if prediction[0] == 1:
                prediction_text = "Result: The person has heart disease."
            else:
                prediction_text = "Result: The person does NOT have heart disease."
        
        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template('heart.html', result=prediction_text)

# 3. Parkinson's Prediction
@app.route('/parkinsons', methods=['GET', 'POST'])
@login_required
def parkinsons():
    prediction_text = ""
    if request.method == 'POST':
        try:
            # Extracting all 22 features from the form
            feature_names = [
                'fo', 'fhi', 'flo', 'jitter_percent', 'jitter_abs', 'rap', 'ppq', 'ddp',
                'shimmer', 'shimmer_db', 'apq3', 'apq5', 'apq', 'dda', 'nhr', 'hnr',
                'rpde', 'dfa', 'spread1', 'spread2', 'd2', 'ppe'
            ]
            
            features = [float(request.form[name]) for name in feature_names]
            
            prediction = parkinsons_model.predict([features])

            if prediction[0] == 1:
                prediction_text = "Result: The person has Parkinson's disease."
            else:
                prediction_text = "Result: The person does NOT have Parkinson's disease."

        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template('parkinsons.html', result=prediction_text)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
