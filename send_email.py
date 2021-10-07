import smtplib
from email.mime.text import MIMEText

def send_message(email, age, height, average_age, average_height, age_count, height_count):
    from_email = "email address here"
    from_password = "email password here"
    to_email = email

    subject = "Age and Height Data"
    message = f"Hey there, your  age is <strong>{age}</strong>, and your height is <strong>{height}</strong>.  " \
              f"The average age of <strong>{age_count}</strong> users is <strong>{average_age}</strong>," \
              f" and the average height of <strong>{height_count}</strong>  users is <strong>{average_height}</strong>."

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)