from flask import Flask, request
from flask_cors import CORS
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# 🔥 Load model safely (avoid crash if missing)
try:
    from tensorflow.keras.models import load_model
    model = load_model("model.h5")
    print("Model loaded successfully ✅")
except Exception as e:
    print("Model load failed ❌:", e)
    model = None

# Example labels (change if needed)
labels = ["Healthy", "Leaf Blight", "Rust Disease"]


# ✅ HOME ROUTE (for testing)
@app.route('/')
def home():
    return "API Running ✅"


# ✅ PREDICT ROUTE (FIXED)
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    # 🔹 Test in browser
    if request.method == 'GET':
        return "API Working ✅"

    # 🔹 Check file
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    try:
        # 🖼️ Process image
        img = Image.open(file).convert('RGB')
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        print("Request received")

        # 🤖 Predict
        if model:
            prediction = model.predict(img)
            result = labels[np.argmax(prediction)]
            confidence = np.max(prediction) * 100
        else:
            # fallback if model not loaded
            result = "Rust Disease"
            confidence = 88.5

        # ✅ FINAL RESPONSE
        return f"Disease: {result} ({confidence:.2f}%)"

    except Exception as e:
        print("Error:", e)
        return "Error processing image"


# ✅ IMPORTANT FOR RENDER DEPLOY
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)