from pypdf import PdfReader
from openai import OpenAI
from pm_os.config import settings
import json
import io

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def parse_credit_agreement(text: str) -> dict:
    """
    Parse credit agreement to extract covenants, terms, and amendments.
    Uses OpenAI API to structure the information.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
        }
    
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        
        system_prompt = """You are a credit analyst extracting structured information from credit agreements and amendments.
Extract the following information in JSON format:

{
  "covenants": [
    {
      "type": "covenant name (e.g., Debt Service Coverage Ratio)",
      "threshold": "the threshold value (e.g., >= 1.25x)",
      "test_frequency": "how often tested (e.g., Quarterly)",
      "cure_period": "cure period if any (e.g., 30 days)",
      "section": "document section reference"
    }
  ],
  "financial_terms": {
    "facility_size": "loan amount",
    "interest_rate": "rate structure",
    "maturity": "maturity date or tenor",
    "security": "collateral/security description",
    "amortization": "amortization schedule"
  },
  "amendments": [
    {
      "section": "section changed",
      "change_description": "what changed",
      "impact": "favorable/neutral/adverse"
    }
  ]
}

If information is not found, use null for that field."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract structured information from this credit agreement:\n\n{text[:15000]}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {
            "error": f"Failed to parse credit agreement: {str(e)}"
        }

def parse_portfolio_report(text: str) -> dict:
    """
    Parse portfolio report to extract financial metrics and company performance.
    Uses OpenAI API to structure the information.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
        }
    
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        
        system_prompt = """You are a financial analyst extracting portfolio company performance metrics.
Extract the following information in JSON format:

{
  "companies": [
    {
      "company": "company name",
      "sector": "industry/sector",
      "investment_date": "date or quarter",
      "invested_capital": numeric value in millions,
      "current_value": numeric value in millions,
      "moic": numeric value (e.g., 1.42),
      "irr": "percentage string (e.g., 27.9%)",
      "ebitda_ltm": numeric value in millions,
      "revenue_growth_yoy": "percentage string (e.g., +46%)",
      "status": "stage (e.g., Growth, Operating)"
    }
  ],
  "fund_summary": {
    "total_invested": numeric value,
    "total_value": numeric value,
    "portfolio_moic": numeric value,
    "top_performers": ["company names"],
    "key_highlights": ["text highlights"]
  }
}

Extract all companies mentioned. Use null if specific metrics not found."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract portfolio metrics from this report:\n\n{text[:15000]}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {
            "error": f"Failed to parse portfolio report: {str(e)}"
        }

def parse_deal_document(text: str) -> dict:
    """
    Parse deal document (CIM, IC memo, etc.) to extract key information.
    Uses OpenAI API to structure the information.
    """
    if not settings.openai_api_key:
        return {
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
        }
    
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        
        system_prompt = """You are an investment analyst extracting key information from deal documents.
Extract the following information in JSON format:

{
  "deal_summary": {
    "company_name": "company name",
    "sector": "industry",
    "deal_type": "equity/credit/other",
    "deal_size": "investment amount"
  },
  "financial_data": {
    "revenue": "revenue figures",
    "ebitda": "EBITDA figures",
    "growth_rate": "growth metrics",
    "valuation": "valuation metrics"
  },
  "key_terms": [
    "list of key deal terms"
  ],
  "risks": [
    "list of identified risks"
  ],
  "tags": [
    "relevant tags/keywords"
  ],
  "extracted_tables": [
    "names of tables found (e.g., Financial Projections, Market Analysis)"
  ]
}

Focus on extracting specific numbers and key terms. Use null if information not found."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract key information from this deal document:\n\n{text[:15000]}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {
            "error": f"Failed to parse deal document: {str(e)}"
        }

