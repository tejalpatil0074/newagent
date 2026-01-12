import streamlit as st 


import streamlit as st
from openai import OpenAI
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenAI SOW Architect",
    page_icon="📄",
    layout="wide"
)

# ---------------- OPENAI HELPER ----------------
def call_openai(prompt, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior enterprise solution architect writing professional Statements of Work."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# ---------------- SESSION STATE ----------------
if "sow" not in st.session_state:
    st.session_state.sow = {}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configuration")
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Paste your OpenAI API key here"
    )

    if openai_api_key:
        st.success("API key loaded")
    else:
        st.warning("API key required")

# ---------------- UI ----------------
st.title("📄 GenAI SOW Architect")
st.caption("End-to-end SOW generator using OpenAI")

tabs = st.tabs(["1️⃣ Generate", "2️⃣ Review", "3️⃣ Export"])

# ================= TAB 1: GENERATE =================
with tabs[0]:
    sol_type = st.selectbox(
        "Solution Type",
        [
            "Intelligent Search",
            "Recommendation System",
            "Virtual Data Analyst",
            "Customer Review Analysis",
            "AI Agents",
            "Other"
        ]
    )

    industry = st.text_input("Industry", "Retail / E-commerce")
    customer = st.text_input("Customer Name", "Acme Corp")

    if st.button("✨ GENERATE SOW CONTENT"):
        if not openai_api_key:
            st.error("Please enter OpenAI API key")
        else:
            with st.spinner("Generating SOW content..."):

                # -------- OBJECTIVE --------
                objective_prompt = f"""
Write EXACTLY 2 professional business sentences for a Statement of Work.

Solution: {sol_type}
Industry: {industry}
Customer: {customer}

Focus on:
- Business outcomes
- Automation
- Measurable value

Do NOT use bullet points.
Do NOT add headings.
"""

                objective = call_openai(objective_prompt, openai_api_key)

                # -------- STAKEHOLDERS --------
                stakeholders_prompt = f"""
List EXACTLY 4 stakeholders for a Statement of Work.

Format strictly as:
Name – Title – Organization

Solution: {sol_type}
Customer: {customer}
"""

                stakeholders = call_openai(stakeholders_prompt, openai_api_key)

                # -------- ASSUMPTIONS & DEPENDENCIES --------
                dependencies_prompt = f"""
Provide EXACTLY the following:

Assumptions:
- 5 items

Dependencies:
- 5 items

Context: {sol_type} AI project.
Keep them project-specific.
"""

                dependencies = call_openai(dependencies_prompt, openai_api_key)

                # -------- TIMELINE --------
                timeline_prompt = f"""
Create a high-level delivery timeline.

Format:
Phase | Activities | Duration

Provide EXACTLY 4 phases.

Solution: {sol_type}
"""

                timeline = call_openai(timeline_prompt, openai_api_key)

                # -------- SAVE --------
                st.session_state.sow = {
                    "solution": sol_type,
                    "industry": industry,
                    "customer": customer,
                    "objective": objective,
                    "stakeholders": stakeholders,
                    "dependencies": dependencies,
                    "timeline": timeline
                }

                st.success("SOW content generated successfully!")

                # DEBUG (VISIBLE)
                st.write("DEBUG Objective:", objective)

# ================= TAB 2: REVIEW =================
with tabs[1]:
    sow = st.session_state.sow

    if not sow:
        st.info("Generate SOW content in Tab 1")
    else:
        st.subheader("Objective")
        sow["objective"] = st.text_area(
            "Edit Objective",
            value=sow["objective"],
            height=100
        )

        st.subheader("Stakeholders")
        sow["stakeholders"] = st.text_area(
            "Edit Stakeholders",
            value=sow["stakeholders"],
            height=150
        )

        st.subheader("Assumptions & Dependencies")
        sow["dependencies"] = st.text_area(
            "Edit Assumptions & Dependencies",
            value=sow["dependencies"],
            height=200
        )

        st.subheader("Timeline")
        sow["timeline"] = st.text_area(
            "Edit Timeline",
            value=sow["timeline"],
            height=200
        )

# ================= TAB 3: EXPORT =================
with tabs[2]:
    sow = st.session_state.sow

    if not sow:
        st.warning("Generate SOW first")
    else:
        html_content = f"""
        <html>
        <body style="font-family:Arial">
        <h1>Statement of Work</h1>
        <p><b>Customer:</b> {sow['customer']}</p>
        <p><b>Industry:</b> {sow['industry']}</p>
        <p><b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}</p>

        <h2>Objective</h2>
        <p>{sow['objective']}</p>

        <h2>Stakeholders</h2>
        <p>{sow['stakeholders'].replace(chr(10), '<br>')}</p>

        <h2>Assumptions & Dependencies</h2>
        <p>{sow['dependencies'].replace(chr(10), '<br>')}</p>

        <h2>Timeline</h2>
        <p>{sow['timeline'].replace(chr(10), '<br>')}</p>
        </body>
        </html>
        """

        st.download_button(
            "📥 Download Word Document",
            data=html_content,
            file_name="SOW.doc",
            mime="application/msword"
        )




