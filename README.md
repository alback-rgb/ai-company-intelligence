# AI Company Intelligence Tool

An AI-powered market intelligence system that automatically collects, analyzes, and generates strategic insights about companies.

This tool gathers information from multiple external sources, processes it using AI models, and produces a structured intelligence report.

It demonstrates the integration of **Python automation, web scraping, API orchestration, and AI-driven analysis** to generate actionable business insights.

---

# Overview

The AI Company Intelligence Tool automates the process of researching companies by collecting data from:

- Company websites
- Search engine results
- Competitor discovery
- Funding signals
- Recent news articles

The collected data is analyzed using **OpenAI GPT models** to generate a structured market intelligence report.

The system then exports the results into structured outputs including **PDF reports and CSV logs**.

---

# Key Features

## Company Website Discovery
Automatically identifies the official company website using Google search via SerpAPI.

## Competitor Discovery
Searches for competitors using Google queries and applies AI filtering to extract real competing companies.

## Funding Signal Detection
Collects signals related to funding, investors, and growth indicators from search results.

## Website Scraping
Extracts and cleans relevant textual content from the company’s official website to provide context for analysis.

## News Monitoring
Uses NewsAPI to collect the latest news articles related to the company.

## AI Market Intelligence Analysis
All collected data is processed using OpenAI models to generate a structured intelligence report including:

- Company Summary
- Industry & Market Context
- Funding & Growth Signals
- Competitor Landscape
- Strategic Signals
- Market Threats
- Automation Opportunities

---

# Automated Report Generation

The system automatically exports the results into:

- **PDF Intelligence Report**
- **CSV Analysis History Log**

This allows tracking historical analyses over time.

---

# Example Output

```
Enter company name: Stripe

Finding company website...
Website: https://stripe.com

Finding competitors...
Competitors: ['PayPal', 'Square', 'Adyen', 'Checkout.com']

Getting funding data...

Scraping website...

Collecting news...

Running AI analysis...

Outputs created:
Stripe_report.pdf
analysis_history.csv
```

---

# Project Structure

```
company-intelligence-tool/

main.py
README.md
analysis_history.csv
.env
```

---

# Installation

Install required dependencies:

```
pip install requests beautifulsoup4 python-dotenv openai reportlab
```

---

# Environment Variables

Create a `.env` file in the project directory:

```
OPENAI_API_KEY=your_openai_key
SERPAPI_KEY=your_serpapi_key
NEWS_API_KEY=your_newsapi_key
```

---

# Usage

Run the tool:

```
python main.py
```

Then enter a company name:

```
Enter company name: Stripe
```

The system will automatically:

1. Discover the company website
2. Identify competitors
3. Gather funding signals
4. Scrape website data
5. Collect recent news
6. Run AI analysis
7. Generate a structured PDF intelligence report

---

# Example Use Cases

This system can be used for:

- Market intelligence
- Competitive analysis
- Startup research
- Sales prospecting
- Investment research
- Strategic business insights
- Venture capital scouting

---

# Technologies Used

Python  
OpenAI API  
SerpAPI  
NewsAPI  
BeautifulSoup  
ReportLab  
dotenv  

---

# Future Improvements

Possible extensions for the project include:

- Competitor website analysis
- LinkedIn company data integration
- Automatic funding round tracking
- Competitor landscape visualization
- Web dashboard interface
- Automated daily monitoring
- Company trend tracking

---

# Author

Built as part of an **AI Automation Portfolio Project**.

The goal of this project is to demonstrate the ability to design **AI-powered intelligence systems that automate complex research and analysis workflows**.
