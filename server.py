import os
import json
from flask import Flask, Response, send_from_directory
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

BASE_URL = "https://pjsbackend.onrender.com"  # Change this when deploying

# Serve images from the static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route("/api/portfolio")
def get_portfolio():
    try:
        tree = ET.parse("portfolio.xml")  # Load XML file
        root = tree.getroot()

        # Loop through each item and modify <media> array
        for item in root.findall("item"):
            media_element = item.find("media")
            if media_element is not None and media_element.text:
                try:
                    media_list = json.loads(media_element.text)  # Convert string back to list
                    updated_media_list = [
                        f"{BASE_URL}{media}" if media.startswith("/static/") else media
                        for media in media_list
                    ]
                    media_element.text = json.dumps(updated_media_list)  # Convert back to string
                except json.JSONDecodeError:
                    print("⚠️ Error decoding media JSON in XML.")

        # Convert modified XML to string and return it
        xml_str = ET.tostring(root, encoding="utf-8").decode()
        return Response(xml_str, mimetype="application/xml")

    except Exception as e:
        return Response(f"<error>Error loading XML: {str(e)}</error>", mimetype="application/xml", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
