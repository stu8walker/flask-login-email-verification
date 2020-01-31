from flask_mail import Message
from app import mail
from flask import current_app
import sys
from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    ) 
    # Send mail async for performance
    # Thread(target=send_async_email, args=(app, msg)).start()
    
    # send non async - slower
    # mail.send(msg)
    
    print('email : ' + msg.recipients[0], file=sys.stdout)
    print('html : ' + msg.html, file=sys.stdout)
    print('subject : ' + msg.subject, file=sys.stdout)
    print('sender : ' + msg.sender, file=sys.stdout)