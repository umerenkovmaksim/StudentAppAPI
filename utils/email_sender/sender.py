import smtplib

from config import EMAIL, PASSWORD

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(EMAIL, PASSWORD)

def send_email(text):
    s.sendmail(EMAIL, "umerenkovmaksim0@gmail.com", text)

s.quit()
