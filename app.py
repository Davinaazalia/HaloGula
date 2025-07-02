from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the model
model = pickle.load(open("rfc_.pkl", "rb"))

app.config["DEBUG"] = True

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # Mengambil data dari form dan mengonversinya ke tipe float
    name = request.form['nama']
    gender = 1 if request.form['gender'] == 'perempuan' else 0
    age = float(request.form['umur'])  # Mengubah nama fitur 'umur' menjadi 'age'
    hypertension = 1 if request.form['hipertensi'] == 'ya' else 0
    heart_disease = 1 if request.form['penyakit_jantung'] == 'ya' else 0
    smoking_history = request.form['riwayat_merokok']
    if smoking_history == "No info":
            smoking_history_encoded = 0
    elif smoking_history == "current":
        smoking_history_encoded = 1
    elif smoking_history == "ever":
        smoking_history_encoded = 2
    elif smoking_history == "former":
        smoking_history_encoded = 3
    elif smoking_history == "never":
        smoking_history_encoded = 4
    elif smoking_history == "not current":
        smoking_history_encoded = 5        
    else:
        smoking_history_encoded = -1
    bmi = float(request.form['bmi'])
    HbA1c_level = float(request.form['hba1c'])
    blood_glucose_level = float(request.form['gula_darah'])


    # Membuat array dari data input
    features = np.array([[gender, age, hypertension, heart_disease,smoking_history_encoded, bmi, HbA1c_level, blood_glucose_level]])

    # Melakukan prediksi dengan model
    prediction = model.predict(features)
# Mapping hasil prediksi ke label teks
    if prediction[0] == 1:
        result = "Diabetes"
        suggestion =("Hasil menunjukkan Anda berisiko terkena diabetes. Kami sarankan Anda untuk mulai mengadopsi gaya hidup sehat."
            "Kurangi konsumsi makanan dan minuman manis, tingkatkan aktivitas fisik secara rutin,"
            "dan perhatikan pola makan teratur. Jika memungkinkan, konsultasikan dengan dokter untuk penanganan lebih lanjut.")
    else:
        result = "Tidak Terkena Diabetes"
        suggestion = ("Hasil menunjukkan Anda tidak berisiko terkena diabetes")


    # Mengembalikan hasil prediksi ke template
    return render_template("index.html",name=name, prediction_text="Prediksi: {}".format(result),suggestion_text=suggestion)

if __name__ == '__main__':

    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))