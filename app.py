from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load model dan label sesuai urutan saat training
model = load_model('modelgigi_cnn.h5')
class_names = ['Calculus', 'Caries', 'Discoloration', 'Normal']  # <- urutan diperbaiki

# Folder upload gambar
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("klasifikasi_gigi.html")

@app.route('/', methods=["POST"])
def predict():
    file = request.files.get('image')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Resize sebelum disimpan
        image_pil = Image.open(file).convert('RGB')  # <-- convert untuk jaga-jaga
        image_pil = image_pil.resize((224, 224))
        image_pil.save(file_path)

        # Preprocess
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # <-- ini wajib!

        # Prediksi
        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_label = class_names[predicted_index]
        confidence = round(float(prediction[predicted_index]) * 100, 2)

        return render_template('klasifikasi_gigi.html',
                               label=predicted_label,
                               confidence=confidence,
                               image_url=file_path)

    return render_template('klasifikasi_gigi.html')

if __name__ == '__main__':
    app.run(debug=True)
