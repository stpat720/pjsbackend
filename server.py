from flask import Flask, Response
from flask_cors import CORS
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)
CORS(app)

@app.route("/api/portfolio")
def get_portfolio():
    try:
        # Reload the XML file every time to ensure it's fresh
        time.sleep(0.5)  # Small delay to prevent reading while being written
        tree = ET.parse("portfolio.xml")
        xml_str = ET.tostring(tree.getroot(), encoding="utf-8").decode()
        return Response(xml_str, mimetype="application/xml")
    except Exception as e:
        return f"Error loading XML: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
