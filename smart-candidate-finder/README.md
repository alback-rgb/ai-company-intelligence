# Smart Candidate Finder

## Overview

Smart Candidate Finder is an AI-powered recruitment automation tool designed to help identify and evaluate potential job candidates from public professional profiles.

The tool searches the web for candidate profiles, extracts relevant information, and uses AI to analyze how well each candidate matches a given job requirement.

This project demonstrates how AI and automation can be combined to streamline the candidate sourcing process.

---

## Features

* Automated candidate discovery from public profiles
* Searches LinkedIn and GitHub using Google search via SerpAPI
* Extracts profile information from search results and profile pages
* AI-powered candidate analysis
* Skill extraction from candidate profiles
* Estimated years of professional experience
* Candidate match scoring
* Ranked candidate output
* Automatic export to CSV

---

## How It Works

1. The user enters:

   * Job title
   * Required skills
   * Target location

2. The system searches the web for candidate profiles using Google search via SerpAPI.

3. Profiles from supported platforms (LinkedIn and GitHub) are collected.

4. The tool extracts text from the profile pages.

5. AI analyzes each candidate and extracts:

   * Name
   * Current role
   * Company
   * Technical skills
   * Estimated years of experience
   * Spoken languages
   * Candidate summary
   * Match score

6. Candidates are ranked based on the AI match score.

7. Results are exported to a CSV file.

---

## Example Usage

Run the tool:

```
python main.py
```

Example input:

```
Enter job title: Python Developer
Enter required skills (comma separated): Python, Django
Enter target location: Germany
```

Example output:

* Ranked list of candidates
* AI-generated candidate summaries
* Candidate skills and estimated experience
* Exported results file: `candidates.csv`

---

## Technologies Used

* Python
* OpenAI API
* SerpAPI
* BeautifulSoup
* Requests
* Web scraping
* AI-powered analysis

---

## Environment Setup

Create a `.env` file in the project directory:

```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key
```

---

## Output

After running the tool, results are saved in:

```
candidates.csv
```

The file includes:

* Candidate name
* Current role
* Company
* Skills
* Estimated years of experience
* Languages
* Match score
* AI summary
* Profile URL

---

## Use Cases

* Recruitment automation
* Talent sourcing
* Candidate screening
* HR technology experimentation
* AI automation portfolio projects

---

Built as part of an AI Automation Portfolio project.
