from flask_mail import Message
from app import mail
from flask import current_app
import sys

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    ) 
    #mail.send(msg)
    print('email : ' + msg.recipients[0], file=sys.stdout)
    print('html : ' + msg.html, file=sys.stdout)
    print('subject : ' + msg.subject, file=sys.stdout)
    print('sender : ' + msg.sender, file=sys.stdout)
    