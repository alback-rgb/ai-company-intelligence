import os
import requests
import csv
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


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

    try:

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return data["organic_results"][0]["link"]

    except Exception as e:

        print("Error finding website:", e)
        return None


# -----------------------------
# Find competitors
# -----------------------------

def find_competitors(company_name):

    url = "https://serpapi.com/search"

    params = {
        "q": company_name + " competitors",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    try:

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        competitors = []

        for result in data.get("organic_results", [])[:5]:
            title = result.get("title", "")
            competitors.append(title)

        return competitors

    except Exception as e:

        print("Error finding competitors:", e)
        return []


# -----------------------------
# Scrape website
# -----------------------------

def scrape_website(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()

        return text[:20000]

    except Exception as e:

        print("Error scraping website:", e)
        return None


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
# AI analysis
# -----------------------------

def analyze_company(text):

    text = text[:6000]

    prompt = f"""
You are a senior business analyst.

Analyze the following company website text.

Return the analysis in this EXACT format:

Company:
Industry:
Market:
Summary:

Strengths:
-

Weaknesses:
-

Pain Points:
-

Automation Opportunities:
-

Website text:
{text}
"""

    try:

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return completion.choices[0].message.content

    except Exception as e:

        print("AI analysis error:", e)
        return None


# -----------------------------
# Save results
# -----------------------------

def save_to_csv(company, website, competitors, analysis):

    file_exists = os.path.isfile("analysis.csv")

    with open("analysis.csv", "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Company",
                "Website",
                "Competitors",
                "Analysis"
            ])

        writer.writerow([
            company,
            website,
            ", ".join(competitors),
            analysis
        ])


# -----------------------------
# Main pipeline
# -----------------------------

def main():

    company = input("Enter company name: ")

    print("\nFinding company website...")

    website = find_company_website(company)

    if not website:
        print("Website not found.")
        return

    print("Website found:", website)

    print("\nFinding competitors...")

    competitors = find_competitors(company)

    print("Competitors found:", competitors)

    print("\nScraping website...")

    text = scrape_website(website)

    if not text:
        print("Could not scrape website.")
        return

    print("Cleaning website text...")

    clean = clean_text(text)

    print("\nAnalyzing company with AI...\n")

    analysis = analyze_company(clean)

    if not analysis:
        print("AI analysis failed.")
        return

    print("Company Intelligence Report\n")

    print(analysis)

    save_to_csv(company, website, competitors, analysis)

    print("\nAnalysis saved to analysis.csv")


if __name__ == "__main__":
    main()