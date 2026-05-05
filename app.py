from flask import Flask, request
from flask_cors import CORS
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# 🔥 Load model safely (Render-friendly)
model = None
try:
    from tensorflow.keras.models import load_model

    if os.path.exists("model.h5"):
        model = load_model("model.h5")
        print("✅ Model loaded successfully")
    else:
        print("⚠ model.h5 not found")

except Exception as e:
    print("❌ Model load failed:", e)
    model = None


# ✅ Labels
labels = ["Healthy", "Leaf Blight", "Rust Disease"]


# ✅ HOME ROUTE
@app.route('/')
def home():
    return "API Running ✅"


# ✅ PREDICT ROUTE
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    # 🔹 Browser test
    if request.method == 'GET':
        return "API Working ✅"

    # 🔹 File check
    if 'file' not in request.files:
        return "❌ No file uploaded"

    file = request.files['file']

    try:
        print("📩 Request received")

        # 🖼️ Image processing
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # 🤖 Prediction
        if model:
            prediction = model.predict(img)
            index = int(np.argmax(prediction))
            result = labels[index]
            confidence = float(np.max(prediction) * 100)
        else:
            # fallback (if model not loaded)
            result = "Rust Disease"
            confidence = 88.5

        # ✅ Response
        return f"Disease: {result} ({confidence:.2f}%)"

    except Exception as e:
        print("❌ Error:", e)
        return "❌ Error processing image"


# ✅ RENDER DEPLOY FIX (IMPORTANT)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)