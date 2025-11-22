import os
import pickle

base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, "saved_models")

diabetes_model = pickle.load(open(os.path.join(model_dir, "diabetes_model.sav"), "rb"))
heart_disease_model = pickle.load(open(os.path.join(model_dir, "heart_model.sav"), "rb"))
parkinsons_model = pickle.load(open(os.path.join(model_dir, "parkinsons_model.sav"), "rb"))
