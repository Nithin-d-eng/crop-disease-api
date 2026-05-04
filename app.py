from flask import Flask, request
from flask_cors import CORS
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# 🔥 LOAD YOUR MODEL (make sure model.h5 is inside C:\flask_app)
model = load_model("model.h5")

# Example labels (change according to your model)
labels = ["Healthy", "Leaf Blight", "Rust Disease"]

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file"

    file = request.files['file']

    # 🖼️ Convert image properly
    img = Image.open(file).convert('RGB')
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    # 🤖 Predict
    prediction = model.predict(img)

    result = labels[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    # ✅ FINAL OUTPUT
    return f"Disease: {result} ({confidence:.2f}%)"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)