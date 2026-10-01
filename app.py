import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st
import config
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview

st.set_page_config(page_title="LegalEase", layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo = config.WEB_LOGO_PATH if config.WEB_LOGO_PATH.exists() else config.LOGO_PATH
    if logo.exists():
        st.image(str(logo))
    else:
        st.markdown("<h1 style='text-align:center;'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    if not all(x.strip() for x in [document_type, parties, terms, dates]):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating document... (10-30 seconds)"):
            try:
                r = requests.post(
                    f"{config.BACKEND_URL}/generate",
                    json={"document_type": document_type, "parties": parties,
                          "terms": terms, "dates": dates},
                    timeout=180,
                )
                if r.status_code == 200:
                    st.session_state.generated_text = sanitize_text(r.json()["document"])
                    st.session_state.doc_type = document_type
                    st.session_state.terms = terms
                    st.session_state.show_edit = False
                else:
                    try:
                        detail = r.json().get("detail", r.text)
                    except Exception:
                        detail = r.text
                    st.error(f"Backend error: {detail}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Make sure the Backend window is running.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

if "generated_text" in st.session_state:
    st.success("✅ Document Generated Successfully!")

    styled = format_html_preview(st.session_state.generated_text)
    st.markdown(
        "<div style='background:#111827;color:#e5e7eb;padding:16px;border-radius:8px;"
        f"max-height:400px;overflow-y:auto;'>{styled}</div>",
        unsafe_allow_html=True,
    )

    if st.button("✏️ Click to Edit Document"):
        st.session_state.show_edit = True

    if st.session_state.get("show_edit"):
        st.session_state.generated_text = st.text_area(
            "Edit Document Below:", st.session_state.generated_text, height=300
        )

    text = st.session_state.generated_text
    dtype = st.session_state.doc_type
    fname = dtype.replace(" ", "_").lower()

    st.download_button("📄 Download as .TXT", data=text, file_name=f"{fname}.txt", mime="text/plain")
    st.download_button(
        "📝 Download as .DOCX",
        data=format_docx(text, dtype, st.session_state.terms),
        file_name=f"{fname}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.download_button(
        "📕 Download as .PDF",
        data=format_pdf(text, dtype, st.session_state.terms),
        file_name=f"{fname}.pdf",
        mime="application/pdf",
    )
else:
    st.info("Click 'Generate Document' to start")
