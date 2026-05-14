from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# HOME ROUTE
@app.route('/')
def home():
    return "API Running ✅"

# PREDICT ROUTE
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'GET':
        return "API Working ✅"

    if 'file' not in request.files:
        return "No file uploaded"

    # TEMP RESULT
    return "Disease: Leaf Blight (92.45%)"

# RUN SERVER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)