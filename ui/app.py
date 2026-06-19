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

/* ---------- BUTTON ---------- */

.stButton > button,
.stFormSubmitButton > button {

    background-color: #C97B63 !important;
    color: white !important;

    border: none !important;
    border-radius: 10px !important;

    height: 42px;

    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {

    background-color: #B86A53 !important;

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

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #E7D9CC;
}

/* ---------- METRICS ---------- */

[data-testid="metric-container"] {

    background: white;

    border: 1px solid #E7D9CC;

    border-radius: 10px;

    padding: 0.75rem;
}

/* ---------- SPINNER ---------- */

[data-testid="stSpinner"] {
    color: #C97B63;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.block-container {
    max-width: 760px;
    padding-top: 4rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stTextInput input {
    border-radius: 10px;
    border: 1px solid #2a2a2a;
    font-size: 15px;
    padding: 0.6rem;
}

.source-pill {
    display: inline-block;
    border: 1px solid #333;
    color: #888;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 20px;
    margin: 4px;
}

.result-section {
    line-height: 1.8;
    font-size: 15px;
}

.small-muted {
    color: #888;
    font-size: 14px;
}

hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# Header

st.title("FailWise")

st.markdown(
    "<p style='color:#6B7280;'>"
    "Explore real engineering failures, incident reports, and postmortems."
    "</p>",
    unsafe_allow_html=True
)

# Stats

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Companies", "12+")

with col2:
    st.metric("Incidents", "100+")

with col3:
    st.metric("Categories", "8+")

st.divider()

# Search Form

with st.form("query_form"):

    question = st.text_input(
        "",
        placeholder="What caused the CircleCI outage in 2025?"
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
        "Search Incidents",
        use_container_width=True
    )

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

st.divider()

st.caption(
    "Built using public engineering postmortems from Cloudflare, AWS, GitHub, Stripe, CircleCI and other infrastructure teams."
)