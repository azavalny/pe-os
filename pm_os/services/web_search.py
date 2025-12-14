from openai import OpenAI
from pm_os.config import settings
import json

def search_portfolio_news(company_names: list[str], themes: list[str]) -> dict:
    """
    Search for power and energy equity research news relevant to portfolio companies
    using OpenAI Responses API with web search.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please add OPENAI_API_KEY to .streamlit/secrets.toml file."
        }
    
    client = OpenAI(api_key=settings.openai_api_key)
    
    company_list = ", ".join(company_names[:10])
    theme_list = ", ".join(set(themes[:15]))
    
    search_query = f"""Look for power and energy equity research news that applies to my thesis and portfolio companies: {company_list}.
    
Focus on themes: {theme_list}

IMPORTANT: Focus on rates of change, momentum, and quantitative metrics (YoY/QoQ growth rates, price changes, volume shifts, market share movements, etc.)

Please structure your response as follows:

## Actionable Investment Insights
[Provide 3-5 key actionable insights with specific rates of change and metrics that impact investment decisions]

## Summary Table: Themes to Companies
[Create a table showing which themes apply to which portfolio companies with the most relevant rate-of-change metrics]

## Detailed News Articles
For each article found:
1. Provide the title and source
2. Highlight specific rates of change and quantitative metrics (e.g., "+25% YoY", "declined 15% QoQ")
3. Explain which portfolio companies this is relevant to and why
4. Identify the main themes covered

Focus on quantitative market developments and rate-of-change analysis."""
    
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
                            "www.woodmac.com"
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

**For EXACTLY 3 COMPANIES, provide:**

### [Company Name] - [Sector/Subsector]
**Portfolio Fit Score: X/10**

- **Location:** [City, Country]
- **Stage:** [Series A/B/C, IPO, Growth, etc.]
- **Recent Metrics:** [Specific growth rates: revenue +X% YoY, funding $X million, MW capacity, etc.]
- **Portfolio Fit Analysis:** [Why this complements existing portfolio - be specific about themes, geography, or capabilities that fill gaps]
- **Recent News:** [Key developments with dates - funding rounds, project wins, expansions]
- **Website:** [If available]

**Scoring Criteria (1-10):**
- Strategic fit with portfolio themes (energy transition, renewables, infrastructure)
- Geographic diversification opportunity
- Growth momentum and market position
- Complementary capabilities vs overlap

Search for companies with:
- Recent funding/IPO announcements (last 12 months)
- Revenue growth >30% YoY
- Operating or expanding in target geographies
- Clear alignment with energy transition themes"""
    
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
                            "www.woodmac.com"
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
