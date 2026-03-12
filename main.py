import os
import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# -----------------------------
# Find company website
# -----------------------------

def find_company_website(company_name):

    url = "https://serpapi.com/search"

    params = {
        "q": company_name + " official website",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data["organic_results"][0]["link"]


# -----------------------------
# Find competitors (raw search)
# -----------------------------

def find_competitors_raw(company_name):

    url = "https://serpapi.com/search"

    params = {
        "q": company_name + " project management competitors",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)

    data = response.json()

    titles = []

    for result in data.get("organic_results", [])[:10]:
        titles.append(result.get("title"))

    return titles


# -----------------------------
# Extract real competitors using AI
# -----------------------------

def extract_real_competitors(company, titles):

    prompt = f"""

From the following search result titles extract ONLY real competing companies.

Company: {company}

Search results:
{titles}

Return a simple list of company names only.

Example:
Asana
Monday
ClickUp
Notion
Trello
"""

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = completion.choices[0].message.content

    competitors = [c.strip("- ").strip() for c in text.split("\n") if c.strip()]

    return competitors


# -----------------------------
# Get funding data
# -----------------------------

def get_funding_data(company):

    url = "https://serpapi.com/search"

    params = {
        "q": company + " funding raised investors",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)

    data = response.json()

    funding = []

    for result in data.get("organic_results", [])[:3]:
        funding.append(result.get("snippet"))

    return funding


# -----------------------------
# Scrape website
# -----------------------------

def scrape_website(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    return text[:20000]


# -----------------------------
# Clean text
# -----------------------------

def clean_text(text):

    lines = text.splitlines()

    cleaned = []

    for line in lines:

        line = line.strip()

        if len(line) > 40:
            cleaned.append(line)

    return " ".join(cleaned)


# -----------------------------
# Get news
# -----------------------------

def get_company_news(company):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": company,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    news = []

    for article in data.get("articles", []):

        news.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "description": article["description"]
        })

    return news


# -----------------------------
# AI analysis
# -----------------------------

def analyze_company(text, company, competitors, funding, news):

    text = text[:6000]

    news_text = ""
    for n in news:
        news_text += f"""
Title: {n['title']}
Source: {n['source']}
Summary: {n['description']}
"""

    funding_text = "\n".join(funding)

    prompt = f"""

You are a senior market intelligence analyst.

Analyze the following company.

Company:
{company}

Competitors:
{competitors}

Funding Data:
{funding_text}

Recent News:
{news_text}

Website Text:
{text}

Return a structured report including:

Company Summary

Industry & Market

Funding & Growth Signals

Competitor Landscape

Strategic Signals

Threats

Automation Opportunities

Also rank the competitors by relevance.

"""

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content


# -----------------------------
# Save history
# -----------------------------

def save_to_csv(company, website, competitors, analysis):

    file_exists = os.path.isfile("analysis_history.csv")

    with open("analysis_history.csv", "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Company",
                "Website",
                "Competitors",
                "Analysis"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            company,
            website,
            ", ".join(competitors),
            analysis
        ])


# -----------------------------
# Generate PDF report
# -----------------------------

def generate_pdf(company, analysis):

    styles = getSampleStyleSheet()

    filename = f"{company}_report.pdf"

    story = []

    story.append(Paragraph(f"{company} Market Intelligence Report", styles["Title"]))

    story.append(Spacer(1, 20))

    for line in analysis.split("\n"):

        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    doc = SimpleDocTemplate(filename)

    doc.build(story)

    print(f"\nPDF report created: {filename}")


# -----------------------------
# Main pipeline
# -----------------------------

def main():

    company = input("Enter company name: ")

    print("\nFinding company website...")
    website = find_company_website(company)
    print("Website:", website)

    print("\nFinding competitors...")
    raw = find_competitors_raw(company)
    competitors = extract_real_competitors(company, raw)
    print("Competitors:", competitors)

    print("\nGetting funding data...")
    funding = get_funding_data(company)

    print("\nScraping website...")
    text = scrape_website(website)
    clean = clean_text(text)

    print("\nCollecting news...")
    news = get_company_news(company)

    print("\nRunning AI analysis...\n")

    analysis = analyze_company(clean, company, competitors, funding, news)

    print(analysis)

    save_to_csv(company, website, competitors, analysis)

    generate_pdf(company, analysis)


if __name__ == "__main__":
    main()