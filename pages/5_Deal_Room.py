import streamlit as st
from pm_os.db import SessionLocal
from pm_os.models import Document, Covenant
from pm_os.services.docqa import generate_ic_memo_outline, answer_question
from pm_os.services.compare import compare_docs, similarity

st.set_page_config(page_title="Deal Library - Private Markets OS", layout="wide", page_icon="📁")

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

st.title("Deal Library - Document Management & Analysis")

st.markdown("---")

companies = [
    {"id": 1, "name": "Roam", "sector": "EV Charging", "status": "Diligence"},
    {"id": 2, "name": "Serra Verde", "sector": "Mining - Rare Earths", "status": "IC Review"},
    {"id": 3, "name": "Virtue Power", "sector": "C&I Solar", "status": "Closed"},
    {"id": 4, "name": "Pontal Energy", "sector": "Renewables", "status": "Portfolio"},
]

mock_documents = {
    "Roam": [
        {
            "name": "Roam CIM.pdf",
            "uploaded": "2024-11-15",
            "extracted_tables": ["Market Analysis", "Financial Summary", "Growth Projections", "Competitive Landscape"],
            "extracted_data": ["Balance Sheet", "P&L Statement", "Cash Flow", "KPIs"],
            "tags": ["Confidential Information Memorandum", "EV Charging", "UK Market", "Growth Strategy"]
        },
        {
            "name": "Roam IC Memo.pdf",
            "uploaded": "2024-12-01",
            "extracted_tables": ["Investment Thesis", "Risk Analysis", "Exit Scenarios"],
            "extracted_data": ["Valuation Model", "Financial Performance Data", "Covenant Analysis"],
            "tags": ["Investment Committee", "Internal Analysis", "Recommendation: Proceed", "IRR Target: 22%"]
        },
        {
            "name": "Roam Management Presentation.pdf",
            "uploaded": "2024-11-20",
            "extracted_tables": ["Network Growth Plan", "Unit Economics"],
            "extracted_data": ["Operations Data", "Customer Data"],
            "tags": ["Management Meeting", "Q4 2024", "Strategic Plan"]
        }
    ],
    "Serra Verde": [
        {
            "name": "Serra Verde Technical Report.pdf",
            "uploaded": "2024-10-10",
            "extracted_tables": ["Resource Estimates", "Production Schedule"],
            "extracted_data": ["Mining Data", "Metallurgical Analysis"],
            "tags": ["Technical Assessment", "Rare Earths", "Brazil"]
        }
    ],
    "Virtue Power": [
        {
            "name": "Virtue Power CIM.pdf",
            "uploaded": "2024-09-05",
            "extracted_tables": ["Pipeline Projects", "Financial Model"],
            "extracted_data": ["Balance Sheet", "Project Data"],
            "tags": ["CIM", "C&I Solar", "IRA Benefits"]
        }
    ],
    "Pontal Energy": [
        {
            "name": "Pontal Q3 2024 Portfolio Update.pdf",
            "uploaded": "2024-10-30",
            "extracted_tables": ["Generation Data", "Revenue Summary"],
            "extracted_data": ["Financial Performance Data", "Operations Data"],
            "tags": ["Portfolio Company", "Quarterly Update", "Wind & Solar"]
        }
    ]
}

st.subheader("Library")

col1, col2 = st.columns([3, 1])
with col1:
    selected_company = st.selectbox(
        "Select Company",
        options=[c["name"] for c in companies],
        format_func=lambda x: f"{x} - {next(c['sector'] for c in companies if c['name'] == x)} ({next(c['status'] for c in companies if c['name'] == x)})"
    )

with col2:
    view_mode = st.radio("View", ["Documents", "Assets"], horizontal=True, label_visibility="collapsed")

st.markdown("---")

documents = mock_documents.get(selected_company, [])

if view_mode == "Documents":
    st.markdown(f"### Documents")
    st.caption(f"All documents ({len(documents)})")
    
    if documents:
        for doc in documents:
            with st.container(border=True):
                col_doc1, col_doc2 = st.columns([3, 1])
                
                with col_doc1:
                    st.markdown(f"**📄 {doc['name']}**")
                    
                    tags_html = " ".join([f'<span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; margin-right: 4px; font-size: 0.85em;">{tag}</span>' for tag in doc['extracted_tables'][:3]])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    
                    if len(doc['extracted_tables']) > 3:
                        st.caption(f"+{len(doc['extracted_tables']) - 3} more tables")
                    
                    data_tags_html = " ".join([f'<span style="background-color: #e1f5fe; padding: 4px 8px; border-radius: 4px; margin-right: 4px; font-size: 0.85em;">{tag}</span>' for tag in doc['extracted_data'][:3]])
                    st.markdown(data_tags_html, unsafe_allow_html=True)
                    
                    st.caption(f"Original uploaded document used for extraction • Uploaded {doc['uploaded']}")
                
                with col_doc2:
                    st.markdown("**Document Actions**")
                    if st.button("View Tables", key=f"tables_{doc['name']}", use_container_width=True):
                        st.session_state['selected_doc'] = doc
                        st.session_state['action'] = 'tables'
                    if st.button("Chat", key=f"chat_{doc['name']}", use_container_width=True):
                        st.session_state['selected_doc'] = doc
                        st.session_state['action'] = 'chat'
                
                with st.expander("Document Details"):
                    st.markdown("**All Extracted Tables:**")
                    for table in doc['extracted_tables']:
                        st.markdown(f"- {table}")
                    
                    st.markdown("**All Extracted Data:**")
                    for data in doc['extracted_data']:
                        st.markdown(f"- {data}")
                    
                    st.markdown("**Tags:**")
                    for tag in doc['tags']:
                        st.markdown(f"- {tag}")
    else:
        st.info(f"No documents uploaded for {selected_company}")

st.markdown("---")

if 'selected_doc' in st.session_state and 'action' in st.session_state:
    doc = st.session_state['selected_doc']
    action = st.session_state['action']
    
    st.subheader(f"{doc['name']}")
    
    tabs = st.tabs(["Q&A", "IC Memo", "Compare", "Covenants"])
    
    with tabs[0]:
        st.subheader("Document Q&A")
        st.write(f"**Selected Document:** {doc['name']}")
        
        q = st.text_input("Ask a question about the document", "What are the key investment highlights?")
        
        if st.button("Answer Question", type="primary"):
            st.markdown("### Answer")
            st.info("Based on the CIM, Roam is the UK's leading long-dwell EV charging network operator with a target of 25,000 chargers. Key investment highlights include: (1) Strong unit economics with average utilization rates improving to 24%, (2) Proprietary software platform providing operational efficiency, (3) Strategic partnerships with major hospitality and residential property owners, (4) Favorable UK policy environment with government EV adoption targets.")
    
    with tabs[1]:
        st.subheader("IC Memo Generator")
        st.write(f"**Selected Document:** {doc['name']}")
        
        if st.button("Generate IC Memo Outline", type="primary"):
            st.success("Memo outline generated!")
            
            st.markdown("## IC Memo: Roam Investment")
            
            st.markdown("### Sections")
            sections = [
                "Executive Summary",
                "Investment Thesis",
                "Market Overview - UK EV Charging",
                "Business Model & Unit Economics",
                "Financial Analysis",
                "Risk Assessment",
                "Exit Strategy",
                "Recommendation"
            ]
            for idx, section in enumerate(sections, 1):
                st.markdown(f"{idx}. {section}")
            
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.markdown("### Key Risks")
                risks = [
                    "EV adoption slower than projected",
                    "Competition from Tesla Supercharger network opening",
                    "Electricity cost inflation",
                    "Utilization rates below target"
                ]
                for risk in risks:
                    st.markdown(f"- {risk}")
            
            with col_m2:
                st.markdown("### Key Questions")
                questions = [
                    "What is the pathway to achieving 25,000 chargers?",
                    "How defensible is the proprietary software advantage?",
                    "What are the site acquisition economics?",
                    "How will open access regulations impact the business?"
                ]
                for question in questions:
                    st.markdown(f"- {question}")
            
            memo_text = f"# IC MEMO: Roam Investment\n\n## Sections\n"
            memo_text += "\n".join([f"{i}. {s}" for i, s in enumerate(sections, 1)])
            memo_text += "\n\n## Key Risks\n" + "\n".join([f"- {r}" for r in risks])
            memo_text += "\n\n## Key Questions\n" + "\n".join([f"- {q}" for q in questions])
            
            st.download_button(
                label="Download Memo Outline",
                data=memo_text,
                file_name=f"ic_memo_{selected_company.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    with tabs[2]:
        st.subheader("Document Comparison")
        
        st.info("Select two documents from the library above to compare")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            doc_a_select = st.selectbox("Document A", [d['name'] for d in documents], key="doc_a")
        with col_c2:
            doc_b_select = st.selectbox("Document B", [d['name'] for d in documents], index=min(1, len(documents)-1), key="doc_b")
        
        if st.button("Compare Documents", type="primary"):
            st.success("Comparison complete!")
            
            st.markdown("### High-Level Changes")
            changes = [
                "Updated financial projections reflect 15% higher revenue in Year 3",
                "Added new risk disclosure regarding regulatory changes",
                "Modified management compensation structure"
            ]
            for change in changes:
                st.markdown(f"- {change}")
            
            st.markdown("### Risk Flags")
            flags = [
                "Covenant headroom reduced from 25% to 18%",
                "Customer concentration increased (top 3 now represent 42% vs 35%)"
            ]
            for flag in flags:
                st.warning(flag)
    
    with tabs[3]:
        st.subheader("Covenant Tracking")
        
        if selected_company == "Roam":
            st.markdown(f"### Covenants for {selected_company}")
            
            covenants = [
                {
                    "type": "Revenue Growth",
                    "threshold": ">= 30% YoY",
                    "frequency": "Quarterly",
                    "next_due": "2025-01-31",
                    "status": "On Track"
                },
                {
                    "type": "Minimum Cash",
                    "threshold": ">= £5,000,000",
                    "frequency": "Monthly",
                    "next_due": "2025-01-31",
                    "status": "Compliant"
                },
                {
                    "type": "Network Growth",
                    "threshold": ">= 1,000 chargers added annually",
                    "frequency": "Annual",
                    "next_due": "2025-12-31",
                    "status": "On Track"
                }
            ]
            
            for cov in covenants:
                with st.expander(f"{cov['type']} | Next Due: {cov['next_due']} | Status: {cov['status']}"):
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        st.markdown(f"**Threshold:** {cov['threshold']}")
                        st.markdown(f"**Test Frequency:** {cov['frequency']}")
                    with col_c2:
                        st.markdown(f"**Next Due Date:** {cov['next_due']}")
                        st.markdown(f"**Status:** {cov['status']}")
        else:
            st.info(f"No covenants tracked for {selected_company}")

st.markdown("---")
st.caption("Document extraction powered by AI • All data encrypted and secure")
