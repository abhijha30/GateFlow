import smtplib
from email.message import EmailMessage

def send_qr(email, file_path):
    try:
        msg = EmailMessage()
        msg['Subject'] = "GateFlow QR Pass"
        msg['From'] = "your_email@gmail.com"
        msg['To'] = email

        msg.set_content("Your QR Pass is attached")

        with open(file_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='png', filename="qr.png")

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Mail error:", e)
        return False
