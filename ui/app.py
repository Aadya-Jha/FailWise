import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from retrieval.chain import ask

load_dotenv()

st.set_page_config(
    page_title="FailWise",
    layout="centered"
)

st.markdown("""
<style>
            
            

/* ---------- PAGE ---------- */

.stApp {
    background-color: #FFF8F2;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ---------- LAYOUT ---------- */

.block-container {
    max-width: 760px;
    padding-top: 4rem;
    padding-bottom: 3rem;
}

/* ---------- TYPOGRAPHY ---------- */

h1 {
    color: #1F2937 !important;
    font-weight: 700 !important;
}

p, label, div {
    color: #374151;
}

.stCaption {
    color: #6B7280;
}

/* ---------- SEARCH INPUT ---------- */

.stTextInput input {
    background-color: white !important;
    color: #1F2937 !important;

    border: 1px solid #E7D9CC !important;
    border-radius: 10px !important;

    padding: 0.8rem !important;
    font-size: 15px !important;

    box-shadow: none !important;
}

.stTextInput input:focus {
    border-color: #C97B63 !important;
    box-shadow: none !important;
}

/* ---------- SELECT BOXES ---------- */

.stSelectbox > div > div {
    background-color: white !important;
    border: 1px solid #E7D9CC !important;
    border-radius: 8px !important;
}

/* ---------- EXPANDER ---------- */

.streamlit-expanderHeader {
    font-weight: 500;
}

/* Popular search buttons */

.stButton > button {
    background: white !important;
    color: #374151 !important;
    border: 1px solid #E7D9CC !important;
    border-radius: 10px !important;
    height: 38px !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #C97B63 !important;
}

/* Search button */

.stFormSubmitButton > button {
    background: #C97B63 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    height: 42px !important;
    font-weight: 600 !important;
    transition: 0.2s ease;
}

.stFormSubmitButton > button:hover {
    background: #B86A53 !important;
    transform: translateY(-1px);
}
            
/* ---------- RESULT AREA ---------- */

.result-section {
    background: white;

    border: 1px solid #E7D9CC;

    border-radius: 12px;

    padding: 1.2rem;

    line-height: 1.8;

    color: #1F2937;

    margin-top: 1rem;
}

/* ---------- SOURCE TAGS ---------- */

.source-pill {

    display: inline-block;

    background: white;

    border: 1px solid #E7D9CC;

    color: #6B7280;

    font-size: 12px;

    padding: 5px 12px;

    border-radius: 999px;

    margin: 4px;
}

.stButton > button {
    background: white !important;
    color: #374151 !important;
    border: 1px solid #E7D9CC !important;
}
            
.stFormSubmitButton > button {
    background: #C97B63 !important;
    color: white !important;
}

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #E7D9CC;
}

/* ---------- SPINNER ---------- */

[data-testid="stSpinner"] {
    color: #C97B63;
}

</style>
""", unsafe_allow_html=True)

# Header

col1, col2 = st.columns([0.7, 12])

with col1:
    st.image("src/failwise.png", width=32)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'>FailWise</h1>
    <p style='color:#6B7280; margin-top:0.25rem;'>
    Explore real engineering failures, incident reports, and postmortems.
    </p>
    """, unsafe_allow_html=True)

# Search Form

with st.form("query_form"):

    question = st.text_input(
    "",
    value=st.session_state.get("question", ""),
    placeholder="Search incidents, outages, and postmortems..."
    )

    st.caption(
        "Examples: Cloudflare DNS failure • GitHub database failover • Stripe API outage"
    )

    with st.expander("Filters"):

        company_filter = st.selectbox(
            "Company",
            [
                "All",
                "Cloudflare",
                "GitHub",
                "AWS",
                "Stripe",
                "Discord",
                "Datadog",
                "Reddit",
                "CircleCI",
                "Slack",
                "Spotify",
                "Zerodha"
            ]
        )

        category_filter = st.selectbox(
            "Category",
            [
                "All",
                "DNS failure",
                "Database outage",
                "Network outage",
                "Configuration failure",
                "Database failover failure",
                "Database migration failure",
                "Distributed systems failure"
            ]
        )

    submitted = st.form_submit_button(
        "Search",
        use_container_width=True
    )

#Example Questions

examples = [
    "What caused the CircleCI outage in 2025?",
    "Why did Cloudflare's DNS fail?",
    "How did GitHub recover from database failovers?",
    "What caused Stripe API outages?",
]

st.markdown("##### Popular searches")

cols = st.columns(2)

for i, example in enumerate(examples):
    with cols[i % 2]:
        if st.button(example, use_container_width=True):
            st.session_state.question = example
            st.rerun()

#Featured Incidents

st.divider()

st.markdown("### Featured Incidents")

st.markdown("""
- **Cloudflare** — Global DNS Outage (2024)
            
- **GitHub** — Database Failover Incident (2023)
            
- **CircleCI** — Build Pipeline Outage (2025)
            
- **Stripe** — API Availability Incident (2022)
""")

# Search Results

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

                result = ask(
                    question,
                    filters if filters else None
                )

                st.divider()

                st.subheader("Analysis")

                st.markdown(
                    f"""
                    <div class="result-section">
                    {result["answer"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if result["sources"]:

                    st.markdown("#### Sources")

                    pills = " ".join(
                        [
                            f'<span class="source-pill">{s.replace(".md", "")}</span>'
                            for s in result["sources"]
                        ]
                    )

                    st.markdown(
                        pills,
                        unsafe_allow_html=True
                    )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )

#Footer

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6B7280;
        padding-top:10px;
        font-size:14px;
    ">
        Built from public postmortems and incident reports from
        <b>Cloudflare</b> ·
        <b>AWS</b> ·
        <b>GitHub</b> ·
        <b>Stripe</b> ·
        <b>CircleCI</b> ·
        <b>Slack</b> ·
        <b>Datadog</b>
    </div>
    """,
    unsafe_allow_html=True
)