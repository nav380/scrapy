import os
import requests
from bs4 import BeautifulSoup
import datetime
import xml.etree.ElementTree as ET
import html

# === CONFIGURATION ===
JOB_ID = "936719006"
BASE_URL = "https://revistas.udca.edu.co/index.php/ruadc"
ARCHIVE_URL = BASE_URL + "/issue/archive"
CURRENT_YEAR = datetime.datetime.now().year
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]  # List of years to scrape  from 2010 to current year

def run_scraper(output_dir=None): # Function to create filestrucutre
    if not output_dir:
        output_dir = JOB_ID
    for year in YEARS:
        os.makedirs(os.path.join(output_dir, year), exist_ok=True)

    def fetch_soup(url):
        resp = requests.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")

    # Get archive page
    archive_soup = fetch_soup(ARCHIVE_URL)
    issues = archive_soup.select("div.archive div.obj_issue_summary")

    results = []

    for issue in issues:
        issue_title = issue.get_text(separator=" ", strip=True)
        issue_link = issue.find("a", href=True)["href"]

        for year in YEARS:
            if year in issue_title:
                year_folder = os.path.join(output_dir, year)
                issue_soup = fetch_soup(issue_link)
                articles = issue_soup.select("div.obj_article_summary")

                for art in articles:
                    title_tag = art.find("h3")
                    if not title_tag:
                        continue

                    title = title_tag.get_text(strip=True)
                    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
                    art_folder = os.path.join(year_folder, safe_title)
                    os.makedirs(art_folder, exist_ok=True)

                    pdf_link_tag = art.find("a", string="PDF")
                    pdf_link = pdf_link_tag["href"] if pdf_link_tag else ""
                    doi_tag = art.find(string=lambda x: x and x.startswith("https://doi.org"))
                    doi = doi_tag.strip() if doi_tag else ""
                    authors_div = art.find("div", class_="authors")
                    authors = authors_div.get_text(separator="; ", strip=True) if authors_div else ""

                    pdf_path = os.path.join(art_folder, safe_title + ".pdf")
                    if pdf_link:
                        pdf_data = requests.get(pdf_link)
                        pdf_data.raise_for_status()
                        with open(pdf_path, "wb") as f:
                            f.write(pdf_data.content)
                        size = os.path.getsize(pdf_path)
                    else:
                        size = "0"

                    # Create XML metadata
                    root = ET.Element("article")
                    metadata = {
                        "title": title,
                        "authors": authors,
                        "affiliation": "",
                        "keywords": "",
                        "pdf_name": os.path.basename(pdf_path),
                        "file_size": str(size),
                        "publication_year": year,
                        "volume": "",
                        "issue": "",
                        "source_id": JOB_ID,
                        "content_provider": "",
                        "doi": doi,
                        "publisher_item_type": "",
                        "start_page": "",
                        "end_page": "",
                        "page_range": "",
                        "abstract": "",
                        "references": "",
                    }
                    for tag, text in metadata.items():
                        el = ET.SubElement(root, tag)
                        el.text = text

                    xml_path = os.path.join(art_folder, safe_title + ".xml")
                    ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

                    # Create HTML summary
                    html_content = f"""<html><head><meta charset="utf-8"><title>{html.escape(title)}</title></head>
<body>
<h1>{html.escape(title)}</h1>
<p><strong>Authors:</strong> {html.escape(authors)}</p>
<p><strong>DOI:</strong> <a href="{html.escape(doi)}">{html.escape(doi)}</a></p>
<p><strong>PDF:</strong> <a href="{os.path.basename(pdf_path)}">{os.path.basename(pdf_path)}</a></p>
</body></html>"""
                    html_path = os.path.join(art_folder, safe_title + ".html")
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    results.append({
                        "year": year,
                        "title": title,
                        "authors": authors,
                        "doi": doi,
                        "pdf_path": pdf_path
                    })

    return results

if __name__ == "__main__":
    data = run_scraper()
    print(f"Scraped {len(data)} articles")
    for item in data:
        print(f"{item['year']} - {item['title']} ({item['doi']})")
