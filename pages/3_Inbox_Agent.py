import streamlit as st
from pm_os.db import SessionLocal
from pm_os.models import Email
import time
import json
import os

st.set_page_config(page_title="Reporting Agent - Private Markets OS", layout="wide", page_icon="📊")

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

st.title("Reporting Agent - Portfolio & Investor Updates")
st.subheader("Automated portfolio reporting and investor communication")

st.markdown("---")

with st.expander("📤 Upload Portfolio Report or Financial Document", expanded=False):
    uploaded_portfolio_file = st.file_uploader(
        "Upload PDF document (portfolio report, quarterly update, financial statement)",
        type=['pdf'],
        key="portfolio_doc_upload",
        help="Upload a portfolio report to extract company performance metrics"
    )
    
    if uploaded_portfolio_file is not None:
        if st.button("Process Document", type="primary", key="process_portfolio_doc"):
            with st.spinner("Extracting text from PDF..."):
                try:
                    from pm_os.services.document_parser import extract_text_from_pdf, parse_portfolio_report
                    
                    extracted_text = extract_text_from_pdf(uploaded_portfolio_file)
                    st.success(f"✓ Extracted {len(extracted_text)} characters from {uploaded_portfolio_file.name}")
                    
                    with st.spinner("Parsing portfolio metrics with AI..."):
                        parsed_data = parse_portfolio_report(extracted_text)
                        
                        if "error" in parsed_data:
                            st.error(parsed_data["error"])
                        else:
                            if 'uploaded_portfolio_docs' not in st.session_state:
                                st.session_state['uploaded_portfolio_docs'] = []
                            
                            st.session_state['uploaded_portfolio_docs'].append({
                                'filename': uploaded_portfolio_file.name,
                                'text': extracted_text,
                                'parsed_data': parsed_data
                            })
                            
                            st.success("✓ Document parsed successfully!")
                            
                            if parsed_data.get('companies'):
                                st.markdown("**Extracted Companies:**")
                                for company in parsed_data['companies'][:3]:
                                    st.markdown(f"- {company.get('company', 'N/A')} - {company.get('sector', 'N/A')}")
                                if len(parsed_data['companies']) > 3:
                                    st.caption(f"+{len(parsed_data['companies']) - 3} more companies")
                            
                            st.rerun()
                            
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

if st.session_state.get('uploaded_portfolio_docs'):
    st.info(f"📄 {len(st.session_state['uploaded_portfolio_docs'])} uploaded document(s) available")
    if st.button("Clear Uploaded Documents", key="clear_portfolio_uploads"):
        st.session_state['uploaded_portfolio_docs'] = []
        st.rerun()

st.markdown("---")

col_report1, col_report2 = st.columns(2)

with col_report1:
    st.subheader("Marking to Market Report")
    st.markdown("Current portfolio valuation and performance metrics")
    
    portfolio_mtm = [
        {
            "company": "Roam",
            "sector": "EV Charging",
            "investment_date": "Q2 2023",
            "invested_capital": 180.0,
            "current_value": 255.0,
            "moic": 1.42,
            "irr": "27.9%",
            "ebitda_ltm": 32.0,
            "revenue_growth_yoy": "+46%",
            "status": "Growth"
        },
        {
            "company": "Serra Verde",
            "sector": "Mining - Rare Earths",
            "investment_date": "Q4 2022",
            "invested_capital": 310.0,
            "current_value": 525.0,
            "moic": 1.69,
            "irr": "35.1%",
            "ebitda_ltm": 82.0,
            "revenue_growth_yoy": "+67%",
            "status": "Pre-Production"
        },
        {
            "company": "Virtue Power",
            "sector": "C&I Solar",
            "investment_date": "Q1 2022",
            "invested_capital": 260.0,
            "current_value": 410.0,
            "moic": 1.58,
            "irr": "28.6%",
            "ebitda_ltm": 61.0,
            "revenue_growth_yoy": "+54%",
            "status": "Operating"
        },
        {
            "company": "Pontal Energy",
            "sector": "Renewables",
            "investment_date": "Q3 2021",
            "invested_capital": 345.0,
            "current_value": 655.0,
            "moic": 1.90,
            "irr": "32.4%",
            "ebitda_ltm": 155.0,
            "revenue_growth_yoy": "+39%",
            "status": "Operating"
        },
        {
            "company": "Ceiba Energy",
            "sector": "Gas & Renewables",
            "investment_date": "Q2 2022",
            "invested_capital": 155.0,
            "current_value": 205.0,
            "moic": 1.32,
            "irr": "21.8%",
            "ebitda_ltm": 48.0,
            "revenue_growth_yoy": "+29%",
            "status": "Development"
        }
    ]
    
    if st.session_state.get('uploaded_portfolio_docs'):
        for doc in st.session_state['uploaded_portfolio_docs']:
            parsed_data = doc.get('parsed_data', {})
            if parsed_data.get('companies'):
                for company_data in parsed_data['companies']:
                    if company_data.get('company'):
                        portfolio_mtm.append({
                            "company": company_data.get('company', 'Unknown'),
                            "sector": company_data.get('sector', 'N/A'),
                            "investment_date": company_data.get('investment_date', 'N/A'),
                            "invested_capital": company_data.get('invested_capital', 0),
                            "current_value": company_data.get('current_value', 0),
                            "moic": company_data.get('moic', 0),
                            "irr": company_data.get('irr', 'N/A'),
                            "ebitda_ltm": company_data.get('ebitda_ltm', 0),
                            "revenue_growth_yoy": company_data.get('revenue_growth_yoy', 'N/A'),
                            "status": company_data.get('status', 'N/A')
                        })
    
    st.markdown("**Q4 2024 Portfolio Summary**")
    st.caption("As of December 14, 2024")
    
    total_invested = sum([p["invested_capital"] for p in portfolio_mtm])
    total_value = sum([p["current_value"] for p in portfolio_mtm])
    total_ebitda = sum([p["ebitda_ltm"] for p in portfolio_mtm])
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        invested_display = f"${total_invested/1000:.2f}B" if total_invested >= 1000 else f"${total_invested:.1f}M"
        st.metric("Invested Capital", invested_display)
    with col_m2:
        value_display = f"${total_value/1000:.2f}B" if total_value >= 1000 else f"${total_value:.1f}M"
        st.metric("Current Value", value_display)
    with col_m3:
        st.metric("Portfolio MOIC", f"{total_value/total_invested:.2f}x")
    
    st.markdown("---")
    
    for company in portfolio_mtm:
        with st.expander(f"**{company['company']}** - {company['sector']}", expanded=False):
            col_c1, col_c2, col_c3 = st.columns(3)
            
            with col_c1:
                st.metric("Invested", f"${company['invested_capital']:.1f}M")
                st.metric("Current Value", f"${company['current_value']:.1f}M")
            
            with col_c2:
                st.metric("MOIC", f"{company['moic']:.2f}x")
                st.metric("IRR", company['irr'])
            
            with col_c3:
                st.metric("EBITDA (LTM)", f"${company['ebitda_ltm']:.1f}M")
                st.metric("Revenue Growth", company['revenue_growth_yoy'])
            
            st.caption(f"Investment Date: {company['investment_date']} | Status: {company['status']}")
    
    st.markdown("---")
    
    with open("data/Example_Marking_to_Market_Report_Sustainable_Infra_Fund_II.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    
    if st.download_button(
        "Export MTM Report",
        pdf_bytes,
        file_name="Marking_to_Market_Report_Q4_2024.pdf",
        mime="application/pdf",
        use_container_width=True
    ):
        st.toast("MTM Report downloaded!", icon="📥")


with col_report2:
    st.subheader("Generate Fundraising Email")
    st.markdown("Weekly investor update email with upcoming calls")
    
    if st.button("Generate Weekly Update Email", type="primary", use_container_width=True, key="generate_email_btn"):
        progress_placeholder = st.empty()
        
        with progress_placeholder.container():
            st.info("Extracting investor calls from Salesforce...")
            time.sleep(3)
        
        progress_placeholder.empty()
        
        st.session_state['generated_email'] = True
        st.rerun()
    
    if st.session_state.get('generated_email', False):
        st.success("Email generated!")
        
        email_content = """**Subject:** Weekly LP Update - Week of December 16, 2024

**To:** Denham Capital Team
**From:** Investor Relations

---

**UPCOMING INVESTOR CALLS THIS WEEK**

We have 3 investor calls scheduled. Below are key talking points:

---

**1. CalPERS - Tuesday, December 17 at 10:00 AM ET**

**Contact:** Jennifer Martinez, Senior Investment Officer
**Fund:** Public Employees' Retirement System
**AUM:** $450B | **Allocation to PE:** ~8%

**Background:**
- Existing LP in Fund VI ($150M commitment)
- Interested in Fund VII for $200M+ commitment
- Focus: Renewable energy and energy transition infrastructure

**Key Topics to Cover:**
- Q4 portfolio performance (highlight Pontal Energy +38% revenue growth)
- Serra Verde rare earths project progress (production timeline)
- Fund VII strategy: increased focus on energy storage and grid infrastructure
- ESG reporting enhancements we've made

**Recent Activity:** Last call was Sept 2024 discussing Fund VII terms

---

**2. Teacher Retirement System of Texas - Wednesday, December 18 at 2:00 PM ET**

**Contact:** Robert Chen, Managing Director - Alternative Investments
**Fund:** TRS Texas
**AUM:** $210B | **Allocation to Infrastructure:** ~6%

**Background:**
- New relationship, introduced via placement agent
- Exploring first commitment to Denham ($100-150M target)
- Strong interest in sustainable infrastructure and mining

**Key Topics to Cover:**
- Firm track record: 15+ year history in energy transition
- Current portfolio highlights: Roam EV charging (28% IRR), Virtue Power solar
- Differentiation: operational value-add and technical expertise
- Fund VII terms and timing (first close Q1 2025)

**Recent Activity:** Initial meeting was Nov 2024, positive feedback received

---

**3. University Endowment - Thursday, December 19 at 11:00 AM ET**

**Contact:** Dr. Sarah Williams, CIO
**Fund:** Major University Endowment
**AUM:** $8.5B | **Allocation to PE/Infra:** ~12%

**Background:**
- Long-term partner: LP in Funds IV, V, and VI
- Strong co-investment track record (participated in 4 deals)
- Seeking $75M commitment to Fund VII plus co-invest rights

**Key Topics to Cover:**
- Fund VI performance update (1.6x MOIC, top quartile tracking)
- Co-investment pipeline for 2025 (Roam follow-on opportunity)
- Impact reporting: renewable energy generation and carbon metrics
- Fund VII portfolio construction strategy

**Recent Activity:** Quarterly update call in Oct 2024

---

**PORTFOLIO HIGHLIGHTS TO EMPHASIZE:**

- **Strong Performance:** Portfolio MOIC of 1.58x across 5 active investments
- **Growth Momentum:** Average revenue growth of 46% YoY across portfolio
- **Energy Transition Focus:** 100% of capital deployed in clean energy value chain
- **Geographic Diversity:** Investments across North America, Latin America, Europe, Africa

**MARKET CONTEXT:**

- Rare earth prices +18% YTD (Serra Verde tailwind)
- EV charging utilization improving to 24% (Roam thesis playing out)
- IRA tax credits extended through 2034 (Virtue Power benefit)

---

**ATTACHMENTS:**
- Q4 2024 Portfolio Performance Deck
- Fund VII Marketing Materials
- ESG Impact Report 2024

Please let me know if you need any additional materials or talking points.

Best regards,
**Investor Relations Team**
"""
        
        st.markdown("---")
        with st.expander("Generated Email", expanded=True):
            st.markdown(email_content)
        
        st.markdown("---")
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.download_button(
                "Download Email",
                email_content,
                file_name="weekly_investor_update.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_e2:
            if st.button("Send to Team", use_container_width=True, key="send_team"):
                st.session_state['email_sent'] = True
                st.rerun()
        
        if st.session_state.get('email_sent', False):
            st.success("✓ Email Sent to Team")

st.markdown("---")