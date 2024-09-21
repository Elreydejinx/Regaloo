from flask_mail import Mail, Message
from flask import url_for

mail = Mail()

def send_notification(recipient_email, unique_id):
    link = url_for('provide_address', unique_id=unique_id, _external=True)
    msg = Message('You have received a gift!',
                  recipients=[recipient_email],
                  body=f'You have received a gift! Please provide your delivery address by visiting the following link: {link}')
    mail.send(msg)
