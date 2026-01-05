from openai import OpenAI
from pm_os.config import settings
import json

def _get_domains_for_verticals(verticals: list[str]) -> list[str]:
    """Get relevant domains based on selected verticals."""
    base_domains = [
        "www.wsj.com",
        "www.bloomberg.com",
        "www.reuters.com",
        "www.ft.com",
        "www.cnbc.com",
        "www.marketwatch.com",
    ]
    
    energy_domains = [
        "www.spglobal.com",
        "www.energy.gov",
        "www.iea.org",
        "www.woodmac.com",
        "www.greentechmedia.com",
        "www.renewableenergyworld.com",
    ]
    
    healthcare_domains = [
        "www.modernhealthcare.com",
        "www.statnews.com",
        "www.fiercehealthcare.com",
        "www.beckershospitalreview.com",
    ]
    
    domains = base_domains.copy()
    
    if "Power & Energy" in verticals:
        domains.extend(energy_domains)
    if "Healthcare" in verticals:
        domains.extend(healthcare_domains)
    if "Power & Energy" not in verticals and "Healthcare" not in verticals:
        domains.append("www.spglobal.com")
    
    return list(set(domains))

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
        return {
            "error": "Please select at least one vertical to search."
        }
    
    verticals_str = ", ".join(verticals)
    allowed_domains = _get_domains_for_verticals(verticals)
    
    is_healthcare_only = verticals == ["Healthcare"]
    is_energy_only = verticals == ["Power & Energy"]
    
    exclusion_note = ""
    if is_healthcare_only:
        exclusion_note = """

**CRITICAL EXCLUSION REQUIREMENTS - STRICTLY ENFORCE:**
- ABSOLUTELY DO NOT include ANY news about: energy, power, renewables, solar, wind, EV charging, battery storage, mining, copper, lithium, energy transition metals, grid infrastructure, or any energy/power infrastructure
- ONLY search for and return healthcare-related news: hospitals, pharmaceuticals, medical devices, biotech, healthcare services, healthcare IT, medical technology, health systems, drug development, clinical trials
- If you find articles mentioning both healthcare AND energy topics, EXCLUDE them entirely - only include pure healthcare content
- If portfolio companies listed are energy-focused, IGNORE them and focus ONLY on general healthcare market trends and healthcare industry developments
- Filter out any results that mention EV charging, renewable energy, solar, wind, battery storage, or mining in the title or content"""
    elif is_energy_only:
        exclusion_note = """

**CRITICAL EXCLUSION REQUIREMENTS:**
- DO NOT include any news about healthcare, hospitals, pharmaceuticals, medical devices, or biotech
- ONLY include energy and power-related news: renewables, solar, wind, EV charging, battery storage, grid infrastructure, mining for energy transition"""
    
    search_query = f"""Look for equity research news EXCLUSIVELY in {verticals_str} that applies to my thesis and portfolio companies: {company_list}.{exclusion_note}
    
Focus on themes: {theme_list}

**CRITICAL FORMATTING REQUIREMENTS:**
- Use standard markdown formatting only (headers, bold, italic, lists, tables)
- NEVER use backticks (`) or code snippet formatting - use plain text for all content
- NO LaTeX equations or mathematical notation - use plain text only (e.g., "+25% YoY" not formulas)
- For dollar amounts, use "USD" prefix or write out "US dollars" instead of "$" symbol (e.g., "1.7 billion USD" or NOT "$1.7 billion")
- NEVER use standalone "$" symbols as they will be interpreted as LaTeX - always use "USD" or "US dollars" for currency
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
                        "allowed_domains": allowed_domains
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


def _get_domains_for_sectors(sectors: list[str]) -> list[str]:
    """Get relevant domains based on selected sectors."""
    base_domains = [
        "www.crunchbase.com",
        "www.pitchbook.com",
        "techcrunch.com",
        "www.bloomberg.com",
        "www.reuters.com",
        "www.ft.com",
        "www.spglobal.com",
    ]
    
    sector_domains = {
        "Solar": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "Wind": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "Energy Storage": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "EV Charging": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "Grid Infrastructure": ["www.greentechmedia.com", "www.renewableenergyworld.com", "www.woodmac.com"],
        "Hydrogen": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "Carbon Capture": ["www.greentechmedia.com", "www.renewableenergyworld.com"],
        "Healthcare Services": ["www.modernhealthcare.com", "www.statnews.com", "www.fiercehealthcare.com", "www.beckershospitalreview.com"],
        "Medical Devices": ["www.modernhealthcare.com", "www.statnews.com", "www.fiercehealthcare.com", "www.beckershospitalreview.com"],
        "Biotech": ["www.modernhealthcare.com", "www.statnews.com", "www.fiercehealthcare.com", "www.beckershospitalreview.com"],
        "Pharmaceuticals": ["www.modernhealthcare.com", "www.statnews.com", "www.fiercehealthcare.com", "www.beckershospitalreview.com"],
        "Healthcare IT": ["www.modernhealthcare.com", "www.statnews.com", "www.fiercehealthcare.com", "www.beckershospitalreview.com"],
    }
    
    domains = base_domains.copy()
    for sector in sectors:
        if sector in sector_domains:
            domains.extend(sector_domains[sector])
    
    return list(set(domains))

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
    
    if not sectors or len(sectors) == 0:
        return {
            "error": "Please select at least one sector to search."
        }
    
    allowed_domains = _get_domains_for_sectors(sectors)
    
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
- Funding: [USD X million in latest round, date] - use "USD" prefix instead of "$" symbol
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
- NEVER use "$" symbol - always use "USD" prefix or "US dollars" for currency amounts (e.g., "USD 50 million" NOT "$50 million")

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
                        "allowed_domains": allowed_domains
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
