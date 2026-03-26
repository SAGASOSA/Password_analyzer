import smtplib
from email.mime.text import MIMEText

def send_otp_email(receiver_email, otp):
    sender_email = "samyakkamble937@gmail.com"
    sender_password = "ireqxgglfzfdrcjt "  # 🔐 paste app password here

    subject = "Password Reset OTP"
    body = f"Your OTP is: {otp}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False