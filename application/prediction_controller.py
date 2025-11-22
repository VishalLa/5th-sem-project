import requests
from flask import (
    render_template,
    url_for,
    redirect,
    Blueprint,
    request,
    current_app as app
)
from .login import login_required

from .load_models import (
    diabetes_model, 
    heart_disease_model, 
    parkinsons_model
)

prediction_controller = Blueprint('prediction_controller', __name__)


# 1. Diabetes Prediction
@prediction_controller.route('/diabetes', methods=['GET', 'POST'])
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
@prediction_controller.route('/heart', methods=['GET', 'POST'])
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
@prediction_controller.route('/parkinsons', methods=['GET', 'POST'])
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

