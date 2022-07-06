import smtplib
from email.message import EmailMessage
from email.utils import formataddr


def notify(body):
    gmail_user = 'python.notification.99@gmail.com'
    gmail_password = 'yleavhdinhfbcled'

    to = 'cdud99@gmail.com'
    subject = 'Web App Updater'

    msg = EmailMessage()
    msg['From'] = formataddr(('Web App Updater', gmail_user))
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, to, msg.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)