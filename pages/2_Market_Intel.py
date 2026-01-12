import streamlit as st
from pm_os.db import SessionLocal
from pm_os.models import MarketSnippet, Deal, Company
from pm_os.services.tagging import tag_text
from pm_os.services.scoring import score_idea
from pm_os.llm.client import LLMClient
from pm_os.services.web_search import search_portfolio_news
from pm_os.config import settings
import json
import os

st.set_page_config(page_title="Market Intel - Private Markets OS", layout="wide", page_icon="📊")

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.page_link("app.py", label="Home", icon="🏠")
    st.markdown("### Tools")
    st.page_link("pages/2_Market_Intel.py", label="Market Intel", icon="📊")
    st.page_link("pages/3_Inbox_Agent.py", label="Reporting Agent", icon="📈")
    st.page_link("pages/4_Credit_Deal_Room.py", label="Credit Origination", icon="💰")
    st.page_link("pages/5_Deal_Room.py", label="Deal Detective", icon="📁")
    st.markdown("---")

llm = LLMClient()
st.title("Market Intelligence - Idea Scoring")
st.subheader("Automate data capture and scoring of new investments")

def load_portfolio_companies():
    portfolio_path = "data/portfolio_companies.json"
    if os.path.exists(portfolio_path):
        with open(portfolio_path, 'r') as f:
            return json.load(f)
    return None

st.markdown("---")

col_main1, col_main2 = st.columns(2)

with col_main1:
    st.subheader("Market Data Search")
    st.markdown("Search for equity research news relevant to portfolio companies")
    
    verticals_filter = st.multiselect(
        "Verticals",
        ["Power & Energy", "Healthcare", "Fintech", "Enterprise Software", "SaaS", "Manufacturing", "Industrial"],
        default=[]
    )
    
    if not settings.openai_api_key:
        st.warning("API key not configured")
    
    if st.button("Run Market Data Search", type="primary", use_container_width=True):
        portfolio_data = load_portfolio_companies()
        
        if portfolio_data:
            companies = portfolio_data.get("companies", [])
            company_list = [c["name"] for c in companies]
            company_themes = []
            for c in companies:
                if c.get("themes"):
                    company_themes.extend(c["themes"])
            
            with st.spinner("Searching trusted financial sources..."):
                result = search_portfolio_news(company_list, company_themes, verticals_filter)
                
                if result.get("error"):
                    st.error(result["error"])
                elif result.get("success"):
                    st.session_state['search_results'] = result
                    st.success("Search completed!")
                    st.rerun()
                else:
                    st.error("Search failed.")
        else:
            st.error("Portfolio companies file not found")
    
    if 'search_results' in st.session_state:
        result = st.session_state['search_results']
        with st.expander("Search Results", expanded=True):
            st.caption("WSJ, Bloomberg, Reuters, Financial Times, CNBC, S&P Global")
            st.markdown("---")
            output_text = result["output"].replace("$", r"\$")
            st.markdown(output_text)
            
            if result.get("sources"):
                st.markdown("---")
                st.caption("**Sources:**")
                for idx, source in enumerate(result["sources"], 1):
                    st.caption(f"{idx}. {source}")
            
            if st.button("Clear Results", key="clear_portfolio"):
                del st.session_state['search_results']
                st.rerun()

with col_main2:
    st.subheader("Investment Discovery")
    st.markdown("AI-powered company search across selected sectors and verticals")
    
    thesis_input = st.text_area(
        "Investment Thesis",
        "Identify high-growth companies with strong unit economics and market positioning.",
        height=80
    )
    
    sectors_filter = st.multiselect(
        "Sectors",
        ["Solar", "Wind", "Energy Storage", "EV Charging", "Grid Infrastructure", "Hydrogen", "Carbon Capture", "Healthcare Services", "Medical Devices", "Biotech", "Pharmaceuticals", "Healthcare IT", "Fintech", "Enterprise Software", "SaaS", "Manufacturing", "Industrial"],
        default=[]
    )
    
    regions_filter = st.multiselect(
        "Regions",
        ["North America", "Europe", "Latin America", "Asia Pacific"],
        default=["North America", "Europe"]
    )
    
    if st.button("Discover Companies", type="primary", use_container_width=True):
        with st.spinner("Searching for opportunities..."):
            from pm_os.services.web_search import search_investment_opportunities
            
            portfolio_data = load_portfolio_companies()
            
            if portfolio_data:
                companies = portfolio_data.get("companies", [])
                
                result_companies = search_investment_opportunities(
                    thesis=thesis_input,
                    sectors=sectors_filter,
                    regions=regions_filter,
                    portfolio_companies=companies
                )
                
                if result_companies.get("success"):
                    st.session_state['company_search_results'] = result_companies
                    st.success("Discovery complete!")
                    st.rerun()
                elif result_companies.get("error"):
                    st.error(result_companies["error"])
                else:
                    st.error("Company search failed.")
            else:
                st.error("Could not load portfolio data")
    
    if 'company_search_results' in st.session_state:
        result_co = st.session_state['company_search_results']
        
        with st.expander("Top Opportunities", expanded=True):
            output_text = result_co["output"].replace("$", r"\$")
            st.markdown(output_text)
            
            if result_co.get("sources"):
                st.markdown("---")
                st.caption("**Sources:**")
                for idx, source in enumerate(result_co["sources"], 1):
                    st.caption(f"{idx}. {source}")
            
            if st.button("Clear Company Results", key="clear_companies"):
                del st.session_state['company_search_results']
                st.rerun()
