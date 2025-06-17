from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return "Barcode Reader API is running"

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        image_url = data.get("image_url")
        if not image_url:
            return jsonify({"error": "No image_url provided"}), 400

        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        decoded = decode(img)

        if not decoded:
            return jsonify({"error": "No barcode detected"}), 404

        results = [{"type": d.type, "data": d.data.decode()} for d in decoded]
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
