AI Company Intelligence Tool

An automated market intelligence tool that collects company data from multiple sources and generates a structured analysis report using AI.

The tool gathers:

Company website information

Competitors

Funding signals

Recent news

Strategic insights

It then produces:

A structured AI-generated company analysis

A PDF report

A CSV history log of all analyses

This project demonstrates Python automation, API integrations, web scraping, and AI-powered analysis.

Features
Company Website Discovery

Automatically finds the official company website using SerpAPI Google search.

Competitor Discovery

Searches Google for competitors and uses AI to extract real competing companies from search results.

Funding Signal Detection

Collects signals about funding and investors from search results.

Website Scraping

Scrapes and cleans text content from the company's website to provide context for analysis.

News Monitoring

Uses NewsAPI to collect the most recent news articles about the company.

AI Market Analysis

The collected data is analyzed using OpenAI GPT models to generate a structured intelligence report including:

Company Summary

Industry & Market

Funding & Growth Signals

Competitor Landscape

Strategic Signals

Threats

Automation Opportunities

Report Generation

The analysis is automatically exported to:

PDF report

CSV history log

Example Output

Running the tool generates:

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
Project Structure
company-intelligence-tool

main.py
README.md
analysis_history.csv (generated automatically)
.env

Required libraries:

requests
beautifulsoup4
python-dotenv
openai
reportlab

3. Create a .env file
OPENAI_API_KEY=your_openai_key
SERPAPI_KEY=your_serpapi_key
NEWS_API_KEY=your_newsapi_key
Usage

Run the program:

python main.py

Then enter a company name:

Enter company name: Stripe

The tool will automatically:

Find the company website

Identify competitors

Gather funding signals

Scrape website data

Collect recent news

Run AI analysis

Generate a PDF report

Example Use Cases

This tool can be used for:

Market intelligence

Competitive analysis

Startup research

Sales prospecting

Investment research

Strategic business insights

Technologies Used

Python

OpenAI API

SerpAPI

NewsAPI

BeautifulSoup

ReportLab

dotenv

Future Improvements

Possible extensions for the project:

Add competitor website analysis

Add company LinkedIn data

Track funding rounds automatically

Visualize competitor landscape

Build a web dashboard

Automate daily monitoring

Author

Built as part of an AI Automation Portfolio project.