import json
import xml.etree.ElementTree as ET

# Load JSON data
with open("data/portfolio.json", "r") as file:
    data = json.load(file)

# Create XML structure
root = ET.Element("portfolio")

for item in data:
    entry = ET.SubElement(root, "item")
    ET.SubElement(entry, "title").text = item["title"]
    ET.SubElement(entry, "description").text = item["description"]
    ET.SubElement(entry, "image").text = item["image"]
    
    categories = ET.SubElement(entry, "categories")
    for category in item["category"]:
        ET.SubElement(categories, "category").text = category

# Save XML
tree = ET.ElementTree(root)
tree.write("portfolio.xml", encoding="utf-8", xml_declaration=True)

print("✅ XML file generated successfully: portfolio.xml")
