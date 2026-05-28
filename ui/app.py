import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from retrieval.chain import ask

load_dotenv()

st.set_page_config(
    page_title="FailWise",
    page_icon="💀",
    layout="centered"
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 760px; }
    .stTextArea textarea { font-family: monospace; font-size: 14px; }
    .source-pill {
        display: inline-block;
        background: #f0f0f0;
        color: #333;
        font-size: 12px;
        font-family: monospace;
        padding: 3px 10px;
        border-radius: 4px;
        margin: 3px 3px 0 0;
    }
    .answer-box {
        background: #fafafa;
        border-left: 3px solid #e0e0e0;
        padding: 1rem 1.25rem;
        font-size: 15px;
        line-height: 1.7;
        border-radius: 0 6px 6px 0;
        margin-top: 1rem;
    }
    h1 { font-size: 1.6rem !important; font-weight: 600 !important; }
    .subtitle { color: #888; font-size: 14px; margin-top: -0.8rem; margin-bottom: 2rem; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 💀 FailWise")
st.markdown('<p class="subtitle">Search engineering postmortems. Ask what went wrong, why, and how teams recovered.</p>', unsafe_allow_html=True)

with st.form("query_form"):
    question = st.text_area(
        "Your question",
        placeholder="e.g. What caused the Cloudflare outage? How did GitHub handle database failovers?",
        height=100,
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        company_filter = st.selectbox(
            "Company",
            ["All", "Cloudflare", "GitHub", "AWS", "Stripe", "Discord",
             "Datadog", "Reddit", "CircleCI", "Slack", "Spotify", "Zerodha"],
            label_visibility="visible"
        )
    with col2:
        category_filter = st.selectbox(
            "Category",
            ["All", "DNS failure", "Database outage", "Network outage",
             "Configuration failure", "Database failover failure",
             "Database migration failure", "Distributed systems failure"],
            label_visibility="visible"
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Search →", use_container_width=True)

if submitted:
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        filters = {}
        if company_filter != "All":
            filters["company"] = company_filter
        if category_filter != "All":
            filters["category"] = category_filter

        with st.spinner("Searching postmortems..."):
            try:
                result = ask(question, filters if filters else None)

                st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

                if result["sources"]:
                    st.markdown("<br>**Sources**", unsafe_allow_html=True)
                    pills = " ".join([
                        f'<span class="source-pill">{s.replace(".md", "")}</span>'
                        for s in result["sources"]
                    ])
                    st.markdown(pills, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.markdown("---")
st.markdown('<p style="color:#bbb; font-size:12px;">Built on real postmortems from Cloudflare, AWS, GitHub, Stripe and others.</p>', unsafe_allow_html=True)