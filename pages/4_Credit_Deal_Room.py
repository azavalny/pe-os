import streamlit as st
import pandas as pd

st.set_page_config(page_title="Credit Deal Room - Private Markets OS", layout="wide", page_icon="💰")

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

st.title("Credit Deal Room - Document Analysis & Monitoring")

st.markdown("---")

credit_tabs = st.tabs(["Covenant Tracking", "Amendment Comparison", "IC Memo Generator"])

# TAB 3: IC Memo Generator
with credit_tabs[2]:
    st.subheader("IC Memo Generator")
    st.caption("Generate structured IC memos from credit agreements")
    
    col_memo1, col_memo2 = st.columns([2, 1])
    with col_memo1:
        memo_deal = st.selectbox(
            "Select Deal",
            ["GridPower Holdings - $150M Senior Secured Credit Facility", "SolarFlex Energy - $85M Term Loan B"],
            key="memo_deal"
        )
    with col_memo2:
        memo_lens = st.selectbox(
            "Analysis Lens",
            ["Balanced", "Conservative", "Downside Case Focus"],
            key="memo_lens"
        )
    
    if st.button("Generate IC Memo Draft", type="primary", key="generate_memo", use_container_width=True):
        with st.spinner("Analyzing credit documents and generating memo..."):
            st.markdown("---")
            st.success("IC Memo draft generated!")
            
            st.markdown("# Investment Committee Memorandum")
            st.markdown(f"**Deal:** {memo_deal}")
            st.markdown(f"**Date:** December 14, 2024")
            st.markdown(f"**Analysis Lens:** {memo_lens}")
            
            st.markdown("---")
            
            with st.expander("### 1. Executive Summary", expanded=True):
                st.markdown("""
**Transaction:** Senior secured credit facility to GridPower Holdings, a renewable energy infrastructure company

**Proposed Terms:**
- **Facility Size:** $150 million term loan
- **Use of Proceeds:** Refinance existing debt ($80M) + fund growth capex ($70M)
- **Tenor:** 5 years
- **Pricing:** SOFR + 450 bps (8.5% all-in)
- **Structure:** First lien on all assets, 50% LTV

**Investment Highlights:**
- Strong asset coverage (1.8x loan-to-appraised-value)
- Diversified revenue across 12 solar/wind projects (95% contracted via PPAs)
- Experienced sponsor with 15-year track record
- Favorable refinancing terms vs. existing facility

**Recommendation:** **APPROVE** with conditions (see Section 8)

*Source: Credit Agreement §1.1, §2.1; Management Presentation Slides 5-8*
                """)
            
            with st.expander("### 2. Business Overview"):
                st.markdown("""
**Company:** GridPower Holdings LLC

**Business Model:**
- Owns and operates 450 MW of renewable energy generation assets
- Portfolio: 8 solar projects (300 MW) + 4 wind projects (150 MW)  
- Geographic concentration: 60% Southeast US, 40% Midwest
- 95% of revenue contracted under 15-20 year PPAs with investment-grade offtakers

**Financial Performance (LTM):**
- Revenue: $68M
- EBITDA: $52M (76% margin)
- Debt Service Coverage Ratio: 1.8x
- Contracted revenue runway: 14 years weighted average

**Management:**
- CEO: Jane Thompson (20 years in renewables, prev. VP at NextEra)
- CFO: Michael Rodriguez (CPA, 12 years project finance)

*Source: CIM Pages 12-18; Management Presentation; Financial Statements*
                """)
            
            with st.expander("### 3. Transaction Structure"):
                st.markdown("""
**Facility Details:**

| Term | Detail |
|------|--------|
| **Facility Type** | Senior Secured Term Loan |
| **Amount** | $150,000,000 |
| **Tenor** | 5 years (maturity Dec 2029) |
| **Amortization** | 10% per year (Years 1-4), balloon at maturity |
| **Interest Rate** | SOFR + 450 bps (floor of 1.0%) |
| **All-in Cost** | ~8.5% (based on current SOFR ~4.0%) |

**Security:**
- First priority lien on all assets (generation facilities, land, equipment, PPAs)
- Pledge of 100% equity interests in borrower
- Debt service reserve account (6 months)

**Use of Proceeds:**
- Refinance existing $80M facility (Bank of America, SOFR+550)
- Growth capital expenditure: $70M for 100 MW solar expansion in Texas

*Source: Credit Agreement §2.1, §2.6, §4.1, §9.1*
                """)
            
            with st.expander("### 4. Key Credit Terms"):
                st.markdown("""
**Financial Covenants:**

| Covenant | Threshold | Test Frequency | Current Headroom |
|----------|-----------|----------------|------------------|
| Debt Service Coverage Ratio | ≥ 1.25x | Quarterly | 44% (1.8x actual) |
| Loan-to-Value | ≤ 60% | Annual | 17% (50% actual) |
| Minimum Liquidity | ≥ $10M | Monthly | 150% ($25M actual) |

**Operational Covenants:**
- Must maintain 90% PPA contract coverage  
- CapEx limited to $20M/year (excluding growth capex from proceeds)
- No asset sales >$10M without lender consent

**Events of Default:**
- Payment default (3-day cure for interest, 5-day for principal)
- Covenant breach (30-day cure for financial covenants)
- Cross-default to other debt >$5M
- Change of control

*Source: Credit Agreement §7.11-7.15 (Covenants); §8.1 (Events of Default)*
                """)
            
            with st.expander("### 5. Financial Overview"):
                st.markdown("""
**Historical Performance:**

| Metric | 2022A | 2023A | LTM Q3'24 |
|--------|-------|-------|-----------|
| Revenue | $58M | $64M | $68M |
| EBITDA | $44M | $48M | $52M |
| EBITDA Margin | 76% | 75% | 76% |
| Debt Service | $28M | $29M | $29M |
| DSCR | 1.57x | 1.66x | 1.79x |

**Projections (Base Case):**

| Metric | 2025E | 2026E | 2027E |
|--------|-------|-------|-------|
| Revenue | $78M | $88M | $92M |
| EBITDA | $60M | $68M | $71M |
| Debt Service | $32M | $34M | $36M |
| DSCR | 1.88x | 2.00x | 1.97x |

**Key Assumptions:**
- Texas expansion online by Q3 2025 (+$12M revenue)
- PPA escalators average 2% annually
- O&M costs remain ~8% of revenue

*Source: Financial Model (attached); Management Projections; Historical Financials*
                """)
            
            with st.expander("### 6. Covenants & Headroom Analysis"):
                st.markdown("""
**Covenant Stress Testing:**

""")
                
                col_cov1, col_cov2 = st.columns(2)
                with col_cov1:
                    st.markdown("""
**DSCR Covenant (≥1.25x):**
- **Current:** 1.79x → **44% headroom**
- **Base Case 2025:** 1.88x → **50% headroom**  
- **Downside Case:** 1.42x → **14% headroom** ✓
- **Breakpoint:** Revenue decline of 30% before breach

*Source: Credit Agreement §7.11; Financial Model sensitivity*
                    """)
                
                with col_cov2:
                    st.markdown("""
**LTV Covenant (≤60%):**
- **Current:** 50% → **17% headroom**
- **Assuming 20% asset value decline:** 58% → **3% headroom** ✓
- **Breakpoint:** Asset value decline of 25% before breach

*Source: Credit Agreement §7.12; Third-party appraisal (Black & Veatch, Sept 2024)*
                    """)
                
                st.warning(f"""
**{memo_lens} View:** The DSCR covenant provides adequate cushion in base case, but only 14% headroom in downside scenario. LTV covenant is more sensitive to asset valuations; a 25% decline would trigger breach. Recommend monitoring PPA counterparty credit and renewable energy asset comps quarterly.
                """)
                
                st.markdown("*Source: Sensitivity Analysis (Financial Model Tab 5)*")
            
            with st.expander("### 7. Risks & Mitigants"):
                col_risk1, col_risk2 = st.columns(2)
                
                with col_risk1:
                    st.markdown("**Key Risks:**")
                    risks = [
                        {
                            "risk": "**Counterparty Credit Risk**",
                            "detail": "Two PPAs (18% of revenue) with single utility (BBB- rated)",
                            "severity": "🟡 Medium"
                        },
                        {
                            "risk": "**Merchant Price Exposure**",
                            "detail": "5% of revenue from merchant sales (wind curtailment)",
                            "severity": "🟡 Medium"
                        },
                        {
                            "risk": "**Development Risk**",
                            "detail": "Texas expansion subject to permitting/construction delays",
                            "severity": "🟠 Medium-High"
                        },
                        {
                            "risk": "**Regulatory Risk**",
                            "detail": "Potential changes to ITC/PTC tax credits",
                            "severity": "🟢 Low (locked in for existing assets)"
                        },
                        {
                            "risk": "**Refinancing Risk**",
                            "detail": "Balloon payment of $90M due in 2029",
                            "severity": "🟡 Medium"
                        }
                    ]
                    for r in risks:
                        st.markdown(f"""
**{r['risk']}**  
{r['detail']}  
*Severity:* {r['severity']}
                        """)
                        st.markdown("---")
                
                with col_risk2:
                    st.markdown("**Mitigants:**")
                    mitigants = [
                        "Utility has maintained investment-grade rating for 15+ years; no signs of distress",
                        "Merchant exposure limited to 5%; ERCOT wind hub pricing remains strong",
                        "Sponsor has delivered 20+ projects on time/budget; general contractor is bonded",
                        "Tax equity structure locked in current ITC rates; sponsor has hedged exposure",
                        "Strong asset coverage (1.8x LTV) and DSCR provides refinancing cushion; 5-year runway to build track record"
                    ]
                    for idx, m in enumerate(mitigants):
                        st.markdown(f"{idx+1}. {m}")
                        st.markdown("---")
                
                st.markdown("*Source: Risk Assessment (Management Discussion); PPA Review; Tax Advisor Memo*")
            
            with st.expander("### 8. Open Questions & Conditions"):
                col_q1, col_q2 = st.columns(2)
                
                with col_q1:
                    st.markdown("**Open Questions for Management:**")
                    questions = [
                        "What is the backup plan if Texas permitting is delayed beyond Q3 2025?",
                        "Has sponsor stress-tested O&M cost inflation scenarios (currently 8% of revenue)?",
                        "What is the expected timeline/strategy for refinancing the 2029 balloon?",
                        "Are there any pending litigation or regulatory investigations?",
                        "What is the capex maintenance plan for aging wind turbines (avg 8 years old)?"
                    ]
                    for idx, q in enumerate(questions, 1):
                        st.markdown(f"{idx}. {q}")
                
                with col_q2:
                    st.markdown("**Approval Conditions:**")
                    conditions = [
                        "✓ Receive updated third-party appraisal (< 6 months old)",
                        "✓ Confirm no Material Adverse Change since LTM financials",
                        "✓ Obtain environmental Phase I reports for all sites",
                        "✓ Require quarterly DSCR reporting (not just annual)",
                        "⚠️ Add covenant: Cap sponsor management fees at 2% of EBITDA"
                    ]
                    for c in conditions:
                        st.markdown(f"- {c}")
            
            st.markdown("---")
            st.markdown("### Recommendation")
            if memo_lens == "Conservative" or memo_lens == "Downside Case Focus":
                st.warning("""
**APPROVE WITH CONDITIONS**

This transaction presents moderate risk-adjusted returns with adequate downside protection. Key strengths include strong asset coverage, high contracted revenue, and experienced sponsor. However, covenant headroom is thinner in downside scenarios, and development risk on the Texas expansion warrants close monitoring.

**Recommended Action:** Approve subject to conditions in Section 8, with quarterly DSCR monitoring and semi-annual asset valuation reviews.

**Vote:** Recommend approval
                """)
            else:
                st.success("""
**APPROVE**

This transaction presents attractive risk-adjusted returns with strong downside protection. Key strengths include robust asset coverage (1.8x LTV), 95% contracted revenue with investment-grade counterparties, and experienced management team. Covenants provide adequate headroom even in stress scenarios.

**Recommended Action:** Approve subject to standard conditions in Section 8.

**Vote:** Recommend approval
                """)
            
            st.markdown("---")
            
            memo_content = f"""# Investment Committee Memorandum
## {memo_deal}
Date: December 14, 2024
Analysis Lens: {memo_lens}

[Full memo content would be exported here]
"""
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "Download IC Memo (Markdown)",
                    memo_content,
                    file_name="ic_memo_gridpower.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_dl2:
                if st.button("Export to Word", use_container_width=True, key="export_word"):
                    st.toast("Word export coming soon!", icon="📄")

# TAB 2: Amendment Comparison
with credit_tabs[1]:
    st.subheader("Amendment / Version Comparison")
    st.caption("Identify meaningful changes and risk implications between document versions")
    
    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        comp_doc1 = st.selectbox(
            "Original Document",
            ["Credit Agreement v1.0 - GridPower (June 2023)", "Credit Agreement v1.0 - SolarFlex (March 2024)"],
            key="comp_doc1"
        )
    with col_comp2:
        comp_doc2 = st.selectbox(
            "Amended Document",
            ["Credit Agreement v2.0 - GridPower (Amendment #1, Nov 2024)", "Credit Agreement v2.0 - SolarFlex (Amendment #1, Sept 2024)"],
            key="comp_doc2"
        )
    
    if st.button("Compare Documents", type="primary", key="compare_credit_docs", use_container_width=True):
        with st.spinner("Performing section-aware comparison..."):
            st.markdown("---")
            st.success("Comparison complete - 8 changes identified")
            
            st.markdown("### What Changed")
            
            changes = [
                {
                    "section": "Section 6.1 - Financial Reporting",
                    "change": "Compliance certificate deadline extended",
                    "detail": "Quarterly compliance certificates due within **45 days** (previously 30 days)",
                    "impact": "neutral",
                    "citation": "Credit Agreement v2.0, §6.1(b)"
                },
                {
                    "section": "Section 7.11 - DSCR Covenant",
                    "change": "DSCR threshold reduced",
                    "detail": "Minimum Debt Service Coverage Ratio reduced to **1.20x** (previously 1.25x)",
                    "impact": "neutral",
                    "citation": "Credit Agreement v2.0, §7.11"
                },
                {
                    "section": "Section 7.14 - Minimum Liquidity",
                    "change": "Liquidity covenant tightened",
                    "detail": "Minimum cash balance increased to **$15M** (previously $10M)",
                    "impact": "adverse",
                    "citation": "Credit Agreement v2.0, §7.14"
                },
                {
                    "section": "Section 1.1 - EBITDA Definition",
                    "change": "EBITDA add-back cap introduced",
                    "detail": "Non-recurring expenses add-back now capped at **$2M per fiscal year** (previously unlimited with lender approval)",
                    "impact": "adverse",
                    "citation": "Credit Agreement v2.0, §1.1 (EBITDA)"
                },
                {
                    "section": "Section 7.2 - CapEx Basket",
                    "change": "CapEx basket increased",
                    "detail": "Annual maintenance CapEx limit increased to **$25M** (previously $20M)",
                    "impact": "neutral",
                    "citation": "Credit Agreement v2.0, §7.2(c)"
                },
                {
                    "section": "Section 2.8 - Prepayment Provisions",
                    "change": "Prepayment penalty period extended",
                    "detail": "Make-whole prepayment period extended to **24 months** (previously 18 months)",
                    "impact": "adverse",
                    "citation": "Credit Agreement v2.0, §2.8"
                },
                {
                    "section": "Section 8.1(h) - Covenant Default Cure Period",
                    "change": "Financial covenant cure period shortened",
                    "detail": "Cure period for financial covenant breaches reduced to **15 days** (previously 30 days)",
                    "impact": "adverse",
                    "citation": "Credit Agreement v2.0, §8.1(h)"
                },
                {
                    "section": "Section 9.12 - Governing Law",
                    "change": "Jurisdiction changed",
                    "detail": "Governing law changed to **Delaware** (previously New York)",
                    "impact": "neutral",
                    "citation": "Credit Agreement v2.0, §9.12"
                }
            ]
            
            for idx, ch in enumerate(changes, 1):
                if ch["impact"] == "adverse":
                    icon = "🔴"
                    color = "#ffebee"
                elif ch["impact"] == "favorable":
                    icon = "🟢"
                    color = "#e8f5e9"
                else:
                    icon = "🟡"
                    color = "#fff9e6"
                
                with st.container(border=True):
                    st.markdown(f"**{icon} Change #{idx}: {ch['section']}**")
                    st.markdown(f"**{ch['change']}**")
                    st.markdown(ch['detail'])
                    st.caption(f"*Source: {ch['citation']}*")
            
            st.markdown("---")
            st.markdown("### Risk Implications")
            
            col_risk1, col_risk2 = st.columns([2, 1])
            with col_risk1:
                st.markdown("#### Key Risk Changes")
                
                st.error("""
**🔴 HIGH PRIORITY: Reduced Covenant Headroom**

The combination of (1) tightened liquidity covenant (+$5M) and (2) EBITDA add-back cap ($2M) meaningfully reduces covenant headroom:

- **Liquidity Headroom:** Reduced from 150% to 67% ($25M actual vs. $15M minimum)
- **DSCR Headroom:** Reduced from 44% to 37% due to EBITDA add-back cap impact
- **Cure Period:** Shortened from 30 to 15 days, reducing reaction time

**Implication:** Company now has less financial flexibility to absorb shocks. In downside case (revenue -20%), liquidity covenant could breach.
                """)
                
                st.warning("""
**🟡 MEDIUM PRIORITY: Increased Monitoring Burden**

- Compliance certificate deadline extension (30→45 days) reduces reporting frequency transparency
- Prepayment penalty extension (18→24 months) limits refinancing optionality
- Net impact: Reduced visibility and flexibility

**Implication:** Lenders should increase quarterly monitoring touchpoints with management.
                """)
                
                st.info("""
**🟢 LOW PRIORITY: Operational Flexibility**

- DSCR covenant relief (1.25x→1.20x) provides modest cushion  
- CapEx basket increase ($20M→$25M) allows for necessary maintenance
- Net impact: Slight improvement in operational flexibility

**Implication:** Management has room for necessary capital investments.
                """)
            
            with col_risk2:
                st.markdown("#### Summary Stats")
                
                st.metric("Total Changes", "8")
                st.metric("Adverse", "4", delta="-50%", delta_color="inverse")
                st.metric("Neutral", "3")
                st.metric("Favorable", "1", delta="+12.5%")
                
                st.markdown("---")
                st.markdown("**Change Distribution**")
                st.markdown("🔴 Adverse: 50%")
                st.progress(0.5)
                st.markdown("🟡 Neutral: 37.5%")
                st.progress(0.375)
                st.markdown("🟢 Favorable: 12.5%")
                st.progress(0.125)
            
            st.markdown("---")
            st.markdown("### Covenant Update Summary")
            
            covenant_changes = {
                "Covenant": ["DSCR", "Minimum Liquidity", "EBITDA Add-backs", "CapEx Limit", "Cure Period"],
                "v1.0": ["≥ 1.25x", "≥ $10M", "Unlimited (w/ approval)", "≤ $20M", "30 days"],
                "v2.0": ["≥ 1.20x", "≥ $15M", "≤ $2M/year", "≤ $25M", "15 days"],
                "Impact": ["🟢 Favorable", "🔴 Adverse", "🔴 Adverse", "🟢 Favorable", "🔴 Adverse"]
            }
            
            df_cov_changes = pd.DataFrame(covenant_changes)
            st.dataframe(df_cov_changes, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            st.markdown("### Recommended Actions")
            st.markdown("""
1. **Request financial projections** reflecting new covenant thresholds to assess headroom
2. **Increase monitoring frequency** to quarterly calls (vs. annual)
3. **Model downside scenarios** with new liquidity covenant ($15M minimum)
4. **Clarify EBITDA add-back cap** - obtain list of add-backs taken in prior periods
5. **Review exit strategy** given extended prepayment penalty period
            """)
            
            comparison_report = """# Amendment Comparison Report
## GridPower Holdings Credit Agreement
### v1.0 (June 2023) vs. v2.0 (Amendment #1, November 2024)

[Full comparison would be exported here]
"""
            
            st.download_button(
                "Download Comparison Report",
                comparison_report,
                file_name="amendment_comparison_gridpower.md",
                mime="text/markdown",
                use_container_width=True
            )

# TAB 1: Covenant Extraction + Auto-Reminders
with credit_tabs[0]:
    st.subheader("Covenant Extraction + Auto-Reminders")
    st.caption("Auto-extracted covenant tracking with compliance monitoring")
    
    deal_select = st.selectbox(
        "Select Deal",
        ["GridPower Holdings - Senior Credit Facility", "SolarFlex Energy - Term Loan B", "WindStream Partners - Revolver"],
        key="covenant_deal"
    )
    
    st.markdown("---")
    st.markdown("### Covenant Summary Table")
    
    if "GridPower" in deal_select:
        covenants_data = {
            "Covenant": [
                "Debt / EBITDA",
                "Interest Coverage (EBITDA / Interest)",
                "Minimum Liquidity",
                "Loan-to-Value",
                "PPA Contract Coverage"
            ],
            "Threshold": [
                "≤ 5.0x",
                "≥ 3.0x",
                "≥ $15,000,000",
                "≤ 60%",
                "≥ 90%"
            ],
            "Test Frequency": [
                "Quarterly",
                "Quarterly",
                "Monthly",
                "Annual",
                "Quarterly"
            ],
            "Next Due": [
                "Jan 15, 2025",
                "Jan 15, 2025",
                "Jan 31, 2025",
                "Mar 31, 2025",
                "Jan 15, 2025"
            ],
            "Current": [
                "3.2x",
                "4.5x",
                "$25.0M",
                "50%",
                "95%"
            ],
            "Headroom": [
                "36%",
                "50%",
                "67%",
                "17%",
                "5.6%"
            ],
            "Status": [
                "✅ Compliant",
                "✅ Compliant",
                "✅ Compliant",
                "✅ Compliant",
                "⚠️ Watch"
            ]
        }
        
        df_covenants = pd.DataFrame(covenants_data)
        
        st.dataframe(
            df_covenants,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", width="small")
            }
        )
        
        st.caption("*Auto-extracted from Credit Agreement v2.0 - GridPower, Sections 7.11-7.15*")
        
        st.markdown("---")
        st.markdown("### Upcoming Compliance Deadlines")
        
        col_dead1, col_dead2, col_dead3 = st.columns(3)
        with col_dead1:
            st.metric("Due This Month", "3", help="Q4 2024 compliance certificates due Jan 15")
        with col_dead2:
            st.metric("Due Next 30 Days", "4", help="Monthly liquidity test due Jan 31")
        with col_dead3:
            st.metric("At Risk", "1", delta="PPA Coverage", delta_color="inverse")
        
        st.markdown("---")
        
        with st.expander("📅 Detailed Covenant Calendar", expanded=True):
            st.markdown("#### January 2025")
            st.markdown("""
- **Jan 15:** Q4 2024 Compliance Certificate due
  - Debt / EBITDA (≤ 5.0x)
  - Interest Coverage (≥ 3.0x)
  - PPA Contract Coverage (≥ 90%)
- **Jan 31:** December 2024 Monthly Liquidity Test (≥ $15M)

#### February 2025
- **Feb 28:** January 2025 Monthly Liquidity Test (≥ $15M)

#### March 2025
- **Mar 31:** Annual Loan-to-Value Test (≤ 60%) - *Requires third-party appraisal*
- **Apr 15:** Q1 2025 Compliance Certificate due
            """)
        
        st.markdown("---")
        st.markdown("### Covenant Deep Dive")
        
        selected_covenant = st.selectbox(
            "Select Covenant for Details",
            ["Debt / EBITDA", "Interest Coverage", "Minimum Liquidity", "Loan-to-Value", "PPA Contract Coverage"],
            key="selected_covenant"
        )
        
        if selected_covenant == "Minimum Liquidity":
            with st.container(border=True):
                st.markdown("#### Minimum Liquidity Covenant")
                
                col_cov1, col_cov2 = st.columns([2, 1])
                with col_cov1:
                    st.markdown("""
**Covenant Definition:**
> The Borrower shall at all times maintain Liquidity (defined as unrestricted cash plus available commitments under the Revolving Credit Facility) of not less than $15,000,000, tested as of the last day of each calendar month.

**Source:** Credit Agreement v2.0, Section 7.14, Page 59

**Test Frequency:** Monthly (last day of month)

**Next Due Date:** January 31, 2025

**Cure Period:** 5 business days
                    """)
                
                with col_cov2:
                    st.metric("Current Liquidity", "$25.0M")
                    st.metric("Minimum Required", "$15.0M")
                    st.metric("Headroom", "$10.0M", delta="67%")
                    st.success("✅ Compliant")
                
                st.markdown("---")
                st.markdown("**Historical Compliance (Last 12 Months)**")
                
                liquidity_data = {
                    "Month": ["Jan'24", "Feb'24", "Mar'24", "Apr'24", "May'24", "Jun'24", "Jul'24", "Aug'24", "Sep'24", "Oct'24", "Nov'24", "Dec'24"],
                    "Actual ($M)": [22.5, 21.8, 23.2, 24.1, 23.8, 25.5, 26.2, 24.8, 25.3, 24.9, 25.1, 25.0],
                    "Status": ["✅"] * 12
                }
                
                df_liquidity = pd.DataFrame(liquidity_data)
                st.dataframe(df_liquidity, use_container_width=True, hide_index=True)
                
                st.info("💡 **Insight:** Liquidity has remained consistently above $20M for the past 12 months, providing comfortable headroom. However, note that v2.0 amendment increased this covenant from $10M to $15M (effective Nov 2024), reducing headroom from 150% to 67%.")
        
        elif selected_covenant == "PPA Contract Coverage":
            with st.container(border=True):
                st.markdown("#### PPA Contract Coverage Covenant")
                
                col_cov1, col_cov2 = st.columns([2, 1])
                with col_cov1:
                    st.markdown("""
**Covenant Definition:**
> The Borrower shall at all times maintain Power Purchase Agreements representing at least 90% of projected annual generation capacity (measured in MWh), tested quarterly.

**Source:** Credit Agreement v2.0, Section 7.15, Page 60

**Test Frequency:** Quarterly

**Next Due Date:** January 15, 2025 (Q4 2024 test)

**Cure Period:** 30 days (must execute replacement PPAs)
                    """)
                
                with col_cov2:
                    st.metric("Current Coverage", "95%")
                    st.metric("Minimum Required", "90%")
                    st.metric("Headroom", "5.6%")
                    st.warning("⚠️ Watch - Low Headroom")
                
                st.markdown("---")
                st.markdown("**PPA Portfolio Breakdown**")
                
                ppa_data = {
                    "Counterparty": ["Duke Energy", "Southern Company", "NextEra", "AEP", "Merchant (ERCOT)"],
                    "Rating": ["A-", "BBB+", "A", "BBB", "N/A"],
                    "Capacity (MW)": [180, 120, 80, 50, 20],
                    "% of Total": ["40%", "27%", "18%", "11%", "4%"],
                    "Expiration": ["2037", "2035", "2039", "2033", "N/A"]
                }
                
                df_ppa = pd.DataFrame(ppa_data)
                st.dataframe(df_ppa, use_container_width=True, hide_index=True)
                
                st.warning("""
⚠️ **Risk Alert:** Only 5.6% headroom on PPA coverage covenant. If any single PPA is terminated or expires without renewal, covenant could breach. AEP contract expires in 2033 (8 years) - earliest expiration in portfolio.

**Recommendation:** Negotiate PPA renewals 24-36 months before expiration to maintain compliance buffer.
                """)
        
        st.markdown("---")
        st.markdown("### Auto-Reminders & Alerts")
        
        with st.container(border=True):
            st.markdown("#### Active Alerts")
            
            st.warning("""
⏰ **UPCOMING: Q4 2024 Compliance Certificate**  
Due: January 15, 2025 (31 days from now)  
Required: Debt/EBITDA, Interest Coverage, PPA Coverage tests  
Action: Request Q4 financials from borrower by Jan 8
            """)
            
            st.info("""
📊 **REMINDER: Monthly Liquidity Test**  
Due: January 31, 2025 (47 days from now)  
Required: Bank statements showing ≥$15M unrestricted cash  
Action: Schedule monthly touch-base with CFO
            """)
            
            st.error("""
🚨 **WATCH: PPA Coverage Covenant Headroom Low**  
Current: 95% (90% required) → Only 5.6% headroom  
Risk: Single PPA termination could cause breach  
Action: Request PPA renewal pipeline update from management
            """)
        
        col_alert1, col_alert2 = st.columns(2)
        with col_alert1:
            if st.button("Export Covenant Calendar (iCal)", use_container_width=True, key="export_ical"):
                st.toast("Calendar export coming soon!", icon="📅")
        with col_alert2:
            if st.button("Configure Email Alerts", use_container_width=True, key="config_alerts"):
                st.toast("Alert configuration coming soon!", icon="🔔")

st.markdown("---")
st.caption("Credit analysis powered by AI • Covenant tracking automated • Risk monitoring 24/7")

