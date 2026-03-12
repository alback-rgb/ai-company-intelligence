import csv
import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from serpapi import GoogleSearch


# ----------------------------------
# LOAD ENV
# ----------------------------------

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
serp_key = os.getenv("SERPAPI_KEY")

client = OpenAI(api_key=openai_key)


# ----------------------------------
# SEARCH CANDIDATES
# ----------------------------------

def search_candidates(job_title, skills, location):

    query = f'{job_title} {skills} {location} site:linkedin.com/in OR site:github.com'

    params = {
        "engine": "google",
        "q": query,
        "api_key": serp_key,
        "num": 20
    }

    search = GoogleSearch(params)
    data = search.get_dict()

    results = []
    seen = set()

    for r in data.get("organic_results", []):

        url = r.get("link", "")

        if url in seen:
            continue

        seen.add(url)

        if not any(domain in url for domain in [
            "linkedin.com/in/",
            "github.com/"
        ]):
            continue

        results.append({
            "title": r.get("title", ""),
            "url": url,
            "snippet": r.get("snippet", "")
        })

    return results


# ----------------------------------
# SCRAPE PROFILE TEXT
# ----------------------------------

def get_profile_text(url):

    try:

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=8)

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        return text[:1500]

    except:
        return ""


# ----------------------------------
# AI ANALYSIS
# ----------------------------------

def analyze_candidate(candidate, job_title, skills):

    profile_text = get_profile_text(candidate["url"])

    prompt = f"""
You are an AI recruiting assistant.

Job title:
{job_title}

Required skills:
{skills}

Candidate headline:
{candidate["title"]}

Search snippet:
{candidate["snippet"]}

Profile text:
{profile_text}

Extract the following:

- candidate name
- current role
- company
- main technical skills
- estimated years of experience
- spoken languages
- short AI summary
- match score (0-100)

Return JSON ONLY:

{{
"name":"",
"current_role":"",
"company":"",
"skills":"",
"years_experience":"",
"languages":"",
"ai_summary":"",
"match_score":0
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except:
        return {
            "name": "Unknown",
            "current_role": "Unknown",
            "company": "Unknown",
            "skills": "",
            "years_experience": "",
            "languages": "",
            "ai_summary": "",
            "match_score": 0
        }


# ----------------------------------
# MAIN
# ----------------------------------

def main():

    job_title = input("Enter job title: ")
    skills = input("Enter required skills (comma separated): ")
    location = input("Enter target location: ")

    print("\nSearching candidates...\n")

    candidates = search_candidates(job_title, skills, location)

    print("Found profiles:", len(candidates))

    results = []

    for c in candidates:

        print("Analyzing:", c["title"])

        analysis = analyze_candidate(c, job_title, skills)

        results.append({
            "name": analysis["name"],
            "role": analysis["current_role"],
            "company": analysis["company"],
            "skills": analysis["skills"],
            "experience": analysis["years_experience"],
            "languages": analysis["languages"],
            "summary": analysis["ai_summary"],
            "score": analysis["match_score"],
            "url": c["url"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    with open("candidates.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Name",
            "Role",
            "Company",
            "Skills",
            "Years Experience",
            "Languages",
            "Score",
            "Summary",
            "URL"
        ])

        for r in results:

            writer.writerow([
                r["name"],
                r["role"],
                r["company"],
                r["skills"],
                r["experience"],
                r["languages"],
                r["score"],
                r["summary"],
                r["url"]
            ])

    print("\nSaved results to candidates.csv\n")

    print("Top Candidates:\n")

    for i, r in enumerate(results[:5], start=1):

        print(f"{i}. {r['name']}")
        print("Role:", r["role"])
        print("Company:", r["company"])
        print("Skills:", r["skills"])
        print("Experience:", r["experience"])
        print("Languages:", r["languages"])
        print("Score:", r["score"])
        print("Profile:", r["url"])
        print()


if __name__ == "__main__":
    main()