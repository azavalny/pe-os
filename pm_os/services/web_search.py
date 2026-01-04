from openai import OpenAI
from pm_os.config import settings
import json

def search_portfolio_news(company_names: list[str], themes: list[str], verticals: list[str] = None) -> dict:
    """
    Search for equity research news relevant to portfolio companies
    using OpenAI Responses API with web search.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please add OPENAI_API_KEY to .streamlit/secrets.toml file."
        }
    
    client = OpenAI(api_key=settings.openai_api_key)
    
    company_list = ", ".join(company_names[:10])
    theme_list = ", ".join(set(themes[:15]))
    
    if verticals is None or len(verticals) == 0:
        verticals = ["Power & Energy"]
    
    verticals_str = ", ".join(verticals)
    
    search_query = f"""Look for equity research news in {verticals_str} that applies to my thesis and portfolio companies: {company_list}.
    
Focus on themes: {theme_list}

**CRITICAL FORMATTING REQUIREMENTS:**
- Use standard markdown formatting only (headers, bold, italic, lists, tables)
- NEVER use backticks (`) or code snippet formatting - use plain text for all content
- NO LaTeX equations or mathematical notation - use plain text only (e.g., "+25% YoY" not formulas)
- Keep responses VERY CONCISE: maximum 1-2 sentences per bullet point
- Focus on rates of change and quantitative metrics (YoY/QoQ growth rates, price changes, volume shifts, market share movements)
- Be brief and direct - avoid verbose explanations

Please structure your response as follows:

## Actionable Investment Insights
- [1-2 sentences max per insight with specific metrics]
- [1-2 sentences max per insight with specific metrics]
- [1-2 sentences max per insight with specific metrics]

## Summary Table: Themes to Companies
[Concise table showing themes → portfolio companies with key metrics]

## Key News Updates
For each relevant article:
- **Title/Source:** [Article title] - [Source]
- **Key Metric:** [1-2 sentences: specific rate of change or quantitative metric]
- **Portfolio Relevance:** [1-2 sentences: which companies and why]

Keep all content brief and focused on quantitative market developments."""
    
    try:
        response = client.responses.create(
            model="gpt-4o",
            tools=[
                {
                    "type": "web_search",
                    "filters": {
                        "allowed_domains": [
                            "www.wsj.com",
                            "www.bloomberg.com",
                            "www.reuters.com",
                            "www.ft.com",
                            "www.cnbc.com",
                            "www.marketwatch.com",
                            "www.spglobal.com",
                            "www.energy.gov",
                            "www.iea.org",
                            "www.woodmac.com",
                            "www.modernhealthcare.com",
                            "www.statnews.com",
                            "www.fiercehealthcare.com",
                            "www.beckershospitalreview.com"
                        ]
                    },
                }
            ],
            tool_choice="auto",
            include=["web_search_call.action.sources"],
            input=search_query,
        )
        
        return {
            "success": True,
            "output": response.output_text,
            "sources": getattr(response, 'sources', []) if hasattr(response, 'sources') else []
        }
        
    except Exception as e:
        return {
            "error": f"Web search failed: {str(e)}"
        }


def search_investment_opportunities(thesis: str, sectors: list[str], regions: list[str], portfolio_companies: list[dict]) -> dict:
    """
    Search for new investment opportunities - actual companies with portfolio fit scores.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please add OPENAI_API_KEY to .streamlit/secrets.toml file."
        }
    
    client = OpenAI(api_key=settings.openai_api_key)
    
    portfolio_summary = []
    for c in portfolio_companies[:10]:
        portfolio_summary.append(f"{c.get('name')} - {c.get('sector')}: {', '.join(c.get('themes', []))}")
    
    search_query = f"""Find ACTUAL COMPANY NAMES for investment opportunities in {', '.join(sectors)} operating in {', '.join(regions)}.

**Current Portfolio Context:**
{chr(10).join(portfolio_summary)}

**Investment Thesis:** {thesis}

**CRITICAL REQUIREMENTS:**
1. Return REAL, SPECIFIC COMPANY NAMES (with full legal names)
2. Focus on emerging and mid-market companies
3. Look for recent funding rounds, IPOs, or growth announcements
4. Score each company 1-10 based on portfolio fit
5. Format as structured company profiles, NOT news articles

**For EXACTLY 3 COMPANIES, use this EXACT format:**

---

## **COMPANY NAME**
**Sector:** [Sector/Subsector] | **Portfolio Fit Score: X/10**

**Location:** [City, Country]  
**Stage:** [Series A/B/C, IPO, Growth, etc.]  
**Website:** [URL if available]

**Business Description:**
[2-3 sentence description of what the company does and its core business model]

**Key Metrics:**
- Revenue Growth: [X% YoY or specific figures]
- Funding: [$X million in latest round, date]
- Other relevant metrics: [MW capacity, customer count, market share, etc.]

**Portfolio Fit Analysis:**
[Why this complements existing portfolio - be specific about themes, geography, or capabilities that fill gaps]

**Recent Developments:**
- [Date] - [Key development: funding round, project win, expansion, etc.]
- [Date] - [Additional development]

---

**IMPORTANT FORMATTING:**
- Use **bold** for company names in headers
- Present information as structured data, not narrative news style
- Focus on facts and metrics, not news article prose
- Each company should be clearly separated with the divider above

**Scoring Criteria (1-10):**
- Strategic fit with portfolio themes and sectors
- Geographic diversification opportunity
- Growth momentum and market position
- Complementary capabilities vs overlap

Search for companies with:
- Recent funding/IPO announcements (last 12 months)
- Revenue growth >30% YoY
- Operating or expanding in target geographies
- Clear alignment with investment thesis and sector focus"""
    
    try:
        response = client.responses.create(
            model="gpt-4o",
            tools=[
                {
                    "type": "web_search",
                    "filters": {
                        "allowed_domains": [
                            "www.crunchbase.com",
                            "www.pitchbook.com",
                            "techcrunch.com",
                            "www.bloomberg.com",
                            "www.reuters.com",
                            "www.ft.com",
                            "www.greentechmedia.com",
                            "www.renewableenergyworld.com",
                            "www.spglobal.com",
                            "www.woodmac.com",
                            "www.modernhealthcare.com",
                            "www.statnews.com",
                            "www.fiercehealthcare.com",
                            "www.beckershospitalreview.com"
                        ]
                    },
                }
            ],
            tool_choice="auto",
            include=["web_search_call.action.sources"],
            input=search_query,
        )
        
        return {
            "success": True,
            "output": response.output_text,
            "sources": getattr(response, 'sources', []) if hasattr(response, 'sources') else []
        }
        
    except Exception as e:
        return {
            "error": f"Investment discovery search failed: {str(e)}"
        }
