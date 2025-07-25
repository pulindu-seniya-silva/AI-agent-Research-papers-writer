import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from langchain.output_parsers import PydanticOutputParser
import pathlib
from datetime import datetime
from fpdf import FPDF

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define output format
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)
format_instructions = parser.get_format_instructions()

def save_to_file(data: ResearchResponse):
    root_dir = pathlib.Path(__file__).parent.resolve()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = root_dir / f"{data.topic.replace(' ', '_')}_research_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📘 Topic: {data.topic}\n\n")
        f.write(f"📄 Summary:\n{data.summary}\n\n")
        f.write(f"📚 Sources:\n" + "\n".join(data.sources) + "\n\n")
        f.write(f"🛠 Tools Used:\n" + ", ".join(data.tools_used))
    st.success(f"✅ Saved to file: {filename}")

def create_pdf(data: ResearchResponse) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Topic: {data.topic}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Summary:\n{data.summary}")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sources:", ln=True)
    pdf.set_font("Arial", "", 12)
    for src in data.sources:
        pdf.multi_cell(0, 8, f"- {src}")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Tools Used:", ln=True)
    pdf.set_font("Arial", "", 12)
    tools_str = ", ".join(data.tools_used) if data.tools_used else "None"
    pdf.multi_cell(0, 10, tools_str)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

# Custom CSS for colors and styling
st.markdown(
    """
    <style>
    .title {
        color: white;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #FFD43B;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.4rem;
    }
    .summary-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333333;
        background-color: #f0f4f8;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        white-space: pre-wrap;
    }
    .footer {
        font-size: 0.9rem;
        color: #888888;
        margin-top: 3rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">🧠AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask your research question and get a structured summary.</div>', unsafe_allow_html=True)

query = st.text_input("🔎 Enter your research query:")

if st.button("Generate Research Paper") and query:
    with st.spinner("Generating response..."):
        prompt = f"""
        You are a research assistant that helps write research papers.
        Wrap the output in the following format and provide no other text:
        {format_instructions}

        Research Topic: {query}
        """
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw_output = response.text

        try:
            structured_response = parser.parse(raw_output)

            st.markdown('<div class="section-header">📘 Topic</div>', unsafe_allow_html=True)
            st.markdown(f"**{structured_response.topic}**")

            st.markdown('<div class="section-header">📄 Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-text">{structured_response.summary}</div>', unsafe_allow_html=True)

            with st.expander(f"📚 Sources ({len(structured_response.sources)})"):
                for src in structured_response.sources:
                    st.write(f"- {src}")

            with st.expander(f"🛠 Tools Used ({len(structured_response.tools_used)})"):
                st.write(", ".join(structured_response.tools_used) if structured_response.tools_used else "None")

            # Store in session state for later buttons
            st.session_state["latest_response"] = structured_response

        except Exception as e:
            st.error(f"Error parsing response: {e}")
            st.text_area("Raw output", raw_output)

if "latest_response" in st.session_state:
    sr = st.session_state["latest_response"]
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save to Text File"):
            save_to_file(sr)

    with col2:
        pdf_bytes = create_pdf(sr)
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_bytes,
            file_name=f"{sr.topic.replace(' ', '_')}_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

st.warning(
    """
    ⚠️ **Important Notice:**  
    This demo uses a limited API key for testing purposes only.  
    Please **do not generate excessive queries** to avoid hitting usage limits.  

    For better and unlimited access,  
    you can download the source code,  
    get your own API key from **Google Gemini**,  
    and update the `.env` file to enjoy full features for free!  

    Thank you for understanding! 🙏
    """
)

st.markdown('<div class="footer">Made by pulindu seniya using Google Gemini API and Streamlit</div>', unsafe_allow_html=True)
