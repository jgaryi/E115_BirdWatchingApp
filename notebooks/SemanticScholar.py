## WEB SCRAPPING OF SEMANTIC SCHOLAR
import os
import re
import time
import requests
import fitz  # PyMuPDF
from fitz import FileDataError
UNPAYWALL_EMAIL = "email@email.com"  #I used my email, please replace by yours

# Conduct search for publication links
def search_semantic_scholar(query="Doliornis sclateri", limit=20):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,url"
    }

    response = requests.get(url, params=params)
    time.sleep(1)  # Delay to reduce chance of 429 Too Many Requests

    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return []

    data = response.json()
    results = []

    for paper in data.get("data", []):
        title = paper.get("title", "No Title")
        link = paper.get("url", "")
        results.append((title, link))

    return results

# Run the search for publication links
results = search_semantic_scholar("Doliornis sclateri", limit=20)

# Display the results of publication links
print(f"\nDisplaying the first {len(results)} Semantic Scholar publications ordered by relevance:\n")
for title, link in results:
    print(f"- {title}\n  {link}")

# For each publication link, search for the download pdf link
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:100] + ".pdf"

def search_semantic_scholar(query="Doliornis sclateri", limit=20):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,url,externalIds"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        time.sleep(1)  # Delay to avoid 429 rate limiting
        if response.status_code != 200:
            return []
        papers = []
        for paper in response.json().get("data", []):
            title = paper.get("title")
            link = paper.get("url")
            doi = paper.get("externalIds", {}).get("DOI")
            papers.append((title, link, doi))
        return papers
    except:
        return []

# If not available, search for the publication using DOI
def get_pdf_from_unpaywall(doi):
    if not doi:
        return None
    try:
        r = requests.get(f"https://api.unpaywall.org/v2/{doi}", params={"email": UNPAYWALL_EMAIL})
        time.sleep(1)  # Delay to avoid unpaywall rate limiting
        if r.status_code == 200:
            data = r.json()
            oa = data.get("best_oa_location")
            return oa.get("url_for_pdf") if oa else None
    except:
        pass
    return None


# Download the pdf of the publications
def download_pdf(title, pdf_url, folder="folder_pdf"):
    if not pdf_url:
        return
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(title)
    filepath = os.path.join(folder, filename)
    try:
        r = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
        time.sleep(1)  # Delay to server
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"Saved in folder_pdf: {filename}")
    except:
        pass

print("PDFs available are being saved in folder_pdf...")
for title, link, doi in results:
    pdf_url = get_pdf_from_unpaywall(doi)
    if pdf_url:
        download_pdf(title, pdf_url)

# Delete corrupted pdfs
def delete_unreadable_pdfs(folder="folder_pdf"):
    for filename in os.listdir(folder):
        if not filename.lower().endswith(".pdf"):
            continue
        path = os.path.join(folder, filename)
        try:
            doc = fitz.open(path)
            if len(doc) == 0:
                raise ValueError("Empty PDF")
            doc.close()
        except Exception:
            os.remove(path)


# Extract texts
def extract_english_text_from_pdfs(folder):
    english_docs = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            try:
                doc = fitz.open(path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
            except FileDataError:
                print(f"Skipped unreadable/corrupted PDF: {file}")
            except Exception as e:
                print(f"Unexpected error reading {file}: {e}")
    return english_docs

# Obtain texts from uncorrupted pdfs
delete_unreadable_pdfs("folder_pdf")
pdf_texts = extract_english_text_from_pdfs("folder_pdf")
