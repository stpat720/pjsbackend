import os
from flask import Flask, Response, send_from_directory
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

BASE_URL = "https://pjsbackend.onrender.com"

# Serve images from the static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route("/api/portfolio")
def get_portfolio():
    try:
        tree = ET.parse("portfolio.xml")
        root = tree.getroot()

        # Convert only relative image paths to full URLs
        for item in root.findall('item'):
            image = item.find('image')
            if image is not None:
                # Ensure only relative paths are modified
                if not image.text.startswith("http"):
                    image.text = f"{BASE_URL}{image.text}"

        xml_str = ET.tostring(root, encoding="utf-8").decode()
        return Response(xml_str, mimetype="application/xml")

    except Exception as e:
        return f"Error loading XML: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
