import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def render_history_download():
    if st.session_state.get("messages"):

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        story = []

        for m in st.session_state.messages:
            role = "User" if m["role"] == "user" else "Assistant"

            # Role heading
            story.append(Paragraph(f"<b>{role}:</b>", styles["Heading4"]))

            # Message text
            story.append(Paragraph(m["content"], styles["Normal"]))

            # Space after each Q/A
            story.append(Spacer(1, 14))   # vertical space

        doc.build(story)
        buffer.seek(0)

        st.download_button(
            "Download Chat History",
            data=buffer,
            file_name="chat_history.pdf",
            mime="application/pdf"
        )
