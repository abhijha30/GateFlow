import smtplib, os
from email.message import EmailMessage

def send_qr(receiver, file):
    msg = EmailMessage()
    msg["Subject"] = "Your GateFlow Pass"
    msg["From"] = os.getenv("EMAIL")
    msg["To"] = receiver

    msg.set_content("Your QR pass is attached.")

    with open(file, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="qr.png")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("APP_PASSWORD"))
        smtp.send_message(msg)
