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
        decoded_objects = decode(img)

        if not decoded_objects:
            return jsonify({"error": "No barcode or QR code detected"}), 404

        results = []
        for obj in decoded_objects:
            results.append({
                "type": obj.type,
                "data": obj.data.decode("utf-8")
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


