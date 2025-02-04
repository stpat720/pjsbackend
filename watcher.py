import time
import json
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to convert JSON to XML
def generate_xml():
    try:
        with open("data/portfolio.json", "r") as file:
            data = json.load(file)

        root = ET.Element("portfolio")

        for item in data:
            entry = ET.SubElement(root, "item")
            ET.SubElement(entry, "title").text = item["title"]
            ET.SubElement(entry, "description").text = item["description"]
            ET.SubElement(entry, "image").text = item["image"]
            
            categories = ET.SubElement(entry, "categories")
            for category in item["category"]:
                ET.SubElement(categories, "category").text = category

        tree = ET.ElementTree(root)
        tree.write("portfolio.xml", encoding="utf-8", xml_declaration=True)
        print("✅ XML updated successfully!")
    except Exception as e:
        print(f"❌ Error generating XML: {e}")

# Handler to watch for file changes
class JSONFileHandler(FileSystemEventHandler):
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
