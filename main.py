from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(...)):
    # 1️⃣ Construct Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    
    # 2️⃣ Fetch HTML content
    response = requests.get(wiki_url)
    if response.status_code != 200:
        return {"error": f"Could not fetch page for {country}"}
    
    # 3️⃣ Parse HTML and extract headings (h1–h6)
    soup = BeautifulSoup(response.text, "html.parser")
    headings = []
    for i in range(1, 7):
        for tag in soup.find_all(f"h{i}"):
            text = tag.get_text().strip()
            if text:
                headings.append(("#" * i) + " " + text)
    
    # 4️⃣ Create Markdown outline
    markdown_outline = "## Contents\n\n" + "\n".join(headings)
    return {"country": country, "outline": markdown_outline}
