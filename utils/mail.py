import smtplib
from email.message import EmailMessage
import streamlit as st

def send_qr(to_email, file_path):
    try:
        EMAIL = st.secrets["abhitheboss2004@gmail.com"]
        PASSWORD = st.secrets["kvdg xpda jyjk bjmu"]

        msg = EmailMessage()
        msg["Subject"] = "🎟 GateFlow Event Pass"
        msg["From"] = EMAIL
        msg["To"] = to_email

        msg.set_content("Your registration is approved ✅\n\nScan attached QR at entry.")

        with open(file_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename="qr.png")

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("MAIL ERROR:", e)
        return False
