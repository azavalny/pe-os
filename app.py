import streamlit as st
from pm_os.config import settings
from pm_os.db import init_db
from pm_os.mock_data import seed_from_csv
import os
from dotenv import load_dotenv

load_dotenv(".env")

st.set_page_config(
    page_title=f"{settings.firm_name} - Private Markets OS",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def bootstrap():
    init_db()
    if not os.path.exists(settings.db_path) or os.path.getsize(settings.db_path) < 5_000:
        seed_from_csv()

bootstrap()

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
    st.page_link("pages/4_Credit_Deal_Room.py", label="Credit Deal Room", icon="💰")
    st.page_link("pages/5_Deal_Room.py", label="Deal Library", icon="📁")
    st.markdown("---")

st.title(f"{settings.firm_name}")
st.subheader("Accelerate deal flow, origination, and portfolio monitoring")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Equity Origination", "Credit Origination", "Investor Relations"])

with tab1:
    st.header("Equity Origination")
    st.markdown("""
    **Market Intelligence & Opportunity Discovery**
    - Monitor portfolio companies with real-time market data
    - AI-powered news analysis with rate-of-change metrics
    - Discover new investment opportunities in energy & renewables
    - Thesis-based company identification and scoring
    - Track themes, metrics, and actionable insights
    """)
    
    if st.button("Open Market Intelligence", type="primary"):
        st.switch_page("pages/2_Market_Intel.py")

with tab2:
    st.header("Credit Origination")
    st.markdown("""
    **Deal Library & Document Management**
    - Document Q&A with AI-powered search
    - IC memo generation and outline creation
    - Document version comparison
    - Financial covenant tracking and monitoring
    
    **Credit Analysis**
    - Automated covenant compliance checking
    - Risk flag identification
    - Amendment impact analysis
    """)
    
    col_credit1, col_credit2 = st.columns(2)
    with col_credit1:
        if st.button("Open Credit Deal Room", type="primary"):
            st.switch_page("pages/4_Credit_Deal_Room.py")
        
with tab3:
    st.header("Investor Relations")
    st.markdown("""
    **Portfolio Reporting & LP Communications**
    - Automated mark-to-market reporting
    - Portfolio performance tracking (MOIC, IRR, EBITDA)
    - Weekly investor update email generation
    - Meeting preparation and talking points
    - Fund performance analytics
    """)
    
    if st.button("Open Reporting Agent", type="primary", use_container_width=True):
        st.switch_page("pages/3_Inbox_Agent.py")

st.markdown("---")
st.caption(f"{settings.firm_name} | Private Markets OS v1.0 MVP")

