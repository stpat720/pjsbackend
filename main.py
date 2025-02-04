from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import xml.etree.ElementTree as ET

app = FastAPI()

# ✅ Allow frontend (Next.js) to connect to backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static images
app.mount("/static", StaticFiles(directory="static"), name="static")

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    portfolio = []
    for item in root.findall("item"):
        portfolio.append({
            "title": item.find("title").text,
            "image": item.find("image").text,  # Image path from XML
            "description": item.find("description").text,
            "category": item.find("category").text.split(",")  # Handle multiple categories
        })
    return portfolio

@app.get("/api/portfolio")
def get_portfolio():
    return parse_xml("portfolio.xml")  # Load XML data from file
