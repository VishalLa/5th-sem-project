Disease Prediction Web Application

This project is a machine-learning powered disease prediction system built as part of the 5th-semester academic requirements. It integrates Flask, ML models, HTML/CSS/JS frontend, and trained classifiers to predict multiple health conditions based on user inputs.

---

## 🚀 Features

- **Multiple Disease Prediction**
  Includes trained ML models for diseases such as diabetes, heart disease, etc.

- **Interactive Web UI**
  User-friendly interface built using Flask templates and JavaScript.

- **Deployed ML Models**
  Models trained using Colab notebooks and integrated for real-time prediction.

- **Modular Project Structure**
  Clean separation of training notebooks, datasets, templates, and application code.

- **Dataset Included**
  Datasets used for academic model training are provided in the `dataset/` folder.

---

## 🛠️ Technologies Used

### Backend
- Python  
- Flask  
- joblib / pickle for saving models

### Machine Learning
- Scikit-Learn  
- Pandas  
- NumPy  

### Frontend
- HTML  
- CSS  
- JavaScript  

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/VishalLa/5th-sem-project.git
cd 5th-sem-project
```

2. Create a virtual environment
```
python -m venv myenv
```

4. Activate the environment

Windows:
```
myenv\Scripts\activate
```

Linux / Mac:
```
source myenv/bin/activate
```
4. Install required packages
```
pip install -r req.txt
```
6. Run the Flask application
```
python app.py
```

7. Open the application in your browser
```
http://127.0.0.1:5000/
```
🤖 Model Training

Training notebooks are located in the colab_files_to_train_models/ folder.

They include:

1. Data cleaning

2. Feature extraction

3. Model training

4. Accuracy evaluation

5. Exporting .pkl model files

To retrain, open the notebooks in Google Colab, run all cells, and download updated model files.

🧪 How Predictions Work

1. User submits medical parameters through a web form.

2. Data is processed and converted to required model format.

3. ML model predicts output (disease/no disease).

4. Result is shown on a results page.
