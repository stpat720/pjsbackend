import time
import json
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

MUX_API_URL = "https://api.mux.com/video/v1/playback-ids/"
MUX_AUTH = ("f7e6509e-8451-42b7-90a1-c6956c1a0627", "tjZlnxHJdBZ6YksqrkJJWSNb11FtX0n07sTK0N35XCVuFbaHxqEZQiMnNUNbnZ6dP2mBg0KPjjl")  # Replace with actual credentials

# Function to fetch aspect ratio from Mux
def get_mux_aspect_ratio(playback_id):
    """Fetches the aspect ratio for a given Mux video playback ID."""
    try:
        if not playback_id:
            return "16/9"  # Default aspect ratio if no valid video ID

        print(f"🔍 Fetching aspect ratio for: {playback_id}")
        
        # Step 1: Fetch asset ID using playback ID
        playback_response = requests.get(
            f"https://api.mux.com/video/v1/playback-ids/{playback_id}", auth=MUX_AUTH
        )

        if playback_response.status_code != 200:
            print(f"⚠️ Warning: Failed to fetch asset ID for {playback_id}. Response: {playback_response.text}")
            return "16/9"

        playback_data = playback_response.json()
        asset_id = playback_data["data"]["object"]["id"]  # Extract asset ID
        print(f"✅ Found Asset ID: {asset_id} for Playback ID: {playback_id}")

        # Step 2: Fetch asset details using asset ID
        asset_response = requests.get(
            f"https://api.mux.com/video/v1/assets/{asset_id}", auth=MUX_AUTH
        )

        if asset_response.status_code != 200:
            print(f"⚠️ Warning: Failed to fetch asset details for {asset_id}. Response: {asset_response.text}")
            return "16/10"

        asset_data = asset_response.json()
        aspect_ratio = asset_data["data"].get("aspect_ratio", "16/9")  # Extract aspect ratio
        
        # Reformat aspect ratio from "16:9" to "16/9"
        aspect_ratio = aspect_ratio.replace(":", "/")
        print(f"✅ Fetched and formatted aspect ratio: {aspect_ratio} for Asset ID: {asset_id}")

        return aspect_ratio

    except Exception as e:
        print(f"❌ Error fetching aspect ratio from Mux: {e}")
        return "16/9"

# Function to convert JSON to XML
def generate_xml():
    """Generates an XML file from the JSON portfolio data."""
    try:
        with open("data/portfolio.json", "r") as file:
            data = json.load(file)

        root = ET.Element("portfolio")

        for item in data:
            entry = ET.SubElement(root, "item")
            ET.SubElement(entry, "title").text = item.get("title", "Untitled")
            ET.SubElement(entry, "description").text = item.get("description", "No description")
            ET.SubElement(entry, "type").text = item.get("type", "still")  # Default to "still" if type is missing
            
            # Ensure mediaSet exists and is a list
            media_set = item.get("mediaset", [])
            print(media_set)

            # Create media array
            media_element = ET.SubElement(entry, "media")
            media_element.text = json.dumps(media_set)

            # Default aspect ratio
            aspect_ratio = "0"  # Default for still images

            if item.get("type") == "still":
                aspect_ratio = "0"  # Not used for stills
            elif item.get("type") in ["motion", "mixed"]:
                if media_set:
                    aspect_ratio = get_mux_aspect_ratio(media_set[0])  # ✅ Pass only the first video ID
                else:
                    aspect_ratio = "16/10"  # Default aspect ratio
                    print("default selected")

            # Add aspect ratio field
            ET.SubElement(entry, "aspect_ratio").text = aspect_ratio
            
            # Add categories
            categories = ET.SubElement(entry, "categories")
            for category in item.get("category", []):
                ET.SubElement(categories, "category").text = category
            
            # Add alternative categories
            if "alt_category" in item and isinstance(item["alt_category"], list):
                alt_categories = ET.SubElement(entry, "alt_categories")
                for alt_category in item["alt_category"]:
                    ET.SubElement(alt_categories, "alt_category").text = alt_category

        tree = ET.ElementTree(root)
        tree.write("portfolio.xml", encoding="utf-8", xml_declaration=True)
        print("✅ XML updated successfully!")
    except Exception as e:
        print(f"❌ Error generating XML: {e}")

# Handler to watch for file changes
class JSONFileHandler(FileSystemEventHandler):
    """Watches for changes in JSON and regenerates XML."""
    def on_modified(self, event):
        if event.src_path.endswith("portfolio.json"):
            print("📢 Detected change in data/portfolio.json. Regenerating XML...")
            generate_xml()

# Start watching portfolio.json in the `data/` folder
if __name__ == "__main__":
    generate_xml()  # Generate XML initially
    event_handler = JSONFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path="data", recursive=False)  # Watch the `data/` directory

    print("👀 Watching for changes in data/portfolio.json...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
